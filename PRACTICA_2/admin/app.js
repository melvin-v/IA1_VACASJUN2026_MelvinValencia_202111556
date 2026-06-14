const API_BASE = "http://localhost:8000";

let token = localStorage.getItem("smartbot_token");
let categoriasCache = [];

const $ = (id) => document.getElementById(id);

async function api(method, path, body) {
  const headers = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const options = { method, headers };
  if (body !== undefined) options.body = JSON.stringify(body);

  const response = await fetch(`${API_BASE}${path}`, options);

  if (response.status === 401) {
    cerrarSesion();
    throw new Error("Sesión expirada");
  }
  if (!response.ok) {
    let detalle = "Error en la solicitud";
    try {
      const data = await response.json();
      detalle = data.detail || detalle;
    } catch (e) {}
    throw new Error(detalle);
  }
  if (response.status === 204) return null;
  return response.json();
}

function mostrarApp() {
  $("login-view").classList.add("hidden");
  $("app-view").classList.remove("hidden");
  cargarEstadisticas();
  cargarCategorias();
  cargarPreguntas();
  cargarConsultas();
  cargarConfiguracion();
}

function mostrarLogin() {
  $("app-view").classList.add("hidden");
  $("login-view").classList.remove("hidden");
}

function cerrarSesion() {
  token = null;
  localStorage.removeItem("smartbot_token");
  mostrarLogin();
}

$("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  $("login-error").textContent = "";
  try {
    const data = await api("POST", "/auth/login", {
      username: $("login-username").value,
      password: $("login-password").value,
    });
    token = data.access_token;
    localStorage.setItem("smartbot_token", token);
    mostrarApp();
  } catch (error) {
    $("login-error").textContent = "Credenciales inválidas";
  }
});

$("logout-btn").addEventListener("click", cerrarSesion);

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
    document.querySelectorAll(".panel").forEach((p) => p.classList.remove("active"));
    tab.classList.add("active");
    $(`tab-${tab.dataset.tab}`).classList.add("active");
  });
});

function escapar(texto) {
  const div = document.createElement("div");
  div.textContent = texto == null ? "" : texto;
  return div.innerHTML;
}

async function cargarEstadisticas() {
  const stats = await api("GET", "/estadisticas");
  $("stats-cards").innerHTML = [
    ["Consultas totales", stats.total_consultas],
    ["Respondidas", stats.consultas_respondidas],
    ["Sin respuesta", stats.consultas_sin_respuesta],
    ["Usuarios únicos", stats.usuarios_unicos],
    ["Preguntas", stats.total_preguntas],
    ["Categorías", stats.total_categorias],
  ]
    .map(
      ([label, value]) =>
        `<div class="card"><div class="value">${value}</div><div class="label">${label}</div></div>`
    )
    .join("");

  $("stats-categorias").innerHTML = renderBarras(stats.consultas_por_categoria);
  $("stats-preguntas").innerHTML = renderBarras(stats.preguntas_mas_consultadas);
}

function renderBarras(items) {
  if (!items.length) return '<li><span class="bar-row"><span>Sin datos aún</span></span></li>';
  const max = Math.max(...items.map((i) => i.cantidad));
  return items
    .map((item) => {
      const ancho = max ? Math.round((item.cantidad / max) * 100) : 0;
      return `<li>
        <div class="bar-row"><span>${escapar(item.etiqueta)}</span><span>${item.cantidad}</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:${ancho}%"></div></div>
      </li>`;
    })
    .join("");
}

async function cargarCategorias() {
  categoriasCache = await api("GET", "/categorias");

  const tbody = $("categorias-table").querySelector("tbody");
  tbody.innerHTML = categoriasCache
    .map(
      (c) => `<tr>
        <td>${escapar(c.nombre)}</td>
        <td>${escapar(c.descripcion)}</td>
        <td class="row-actions">
          <button class="link-btn" onclick="editarCategoria(${c.id})">Editar</button>
          <button class="link-btn danger" onclick="eliminarCategoria(${c.id})">Eliminar</button>
        </td>
      </tr>`
    )
    .join("");

  $("pregunta-categoria").innerHTML = categoriasCache
    .map((c) => `<option value="${c.id}">${escapar(c.nombre)}</option>`)
    .join("");
}

$("categoria-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const id = $("categoria-id").value;
  const body = {
    nombre: $("categoria-nombre").value,
    descripcion: $("categoria-descripcion").value,
  };
  try {
    if (id) {
      await api("PUT", `/categorias/${id}`, body);
    } else {
      await api("POST", "/categorias", body);
    }
    resetCategoriaForm();
    cargarCategorias();
  } catch (error) {
    alert(error.message);
  }
});

function editarCategoria(id) {
  const cat = categoriasCache.find((c) => c.id === id);
  if (!cat) return;
  $("categoria-id").value = cat.id;
  $("categoria-nombre").value = cat.nombre;
  $("categoria-descripcion").value = cat.descripcion || "";
  $("categoria-submit").textContent = "Guardar";
  $("categoria-cancel").classList.remove("hidden");
}

async function eliminarCategoria(id) {
  if (!confirm("¿Eliminar esta categoría y sus preguntas?")) return;
  try {
    await api("DELETE", `/categorias/${id}`);
    cargarCategorias();
    cargarPreguntas();
  } catch (error) {
    alert(error.message);
  }
}

function resetCategoriaForm() {
  $("categoria-id").value = "";
  $("categoria-form").reset();
  $("categoria-submit").textContent = "Agregar";
  $("categoria-cancel").classList.add("hidden");
}

$("categoria-cancel").addEventListener("click", resetCategoriaForm);

let preguntasCache = [];

async function cargarPreguntas() {
  preguntasCache = await api("GET", "/preguntas");
  const tbody = $("preguntas-table").querySelector("tbody");
  tbody.innerHTML = preguntasCache
    .map((p) => {
      const cat = categoriasCache.find((c) => c.id === p.categoria_id);
      const nombreCat = cat ? cat.nombre : "—";
      return `<tr>
        <td>${escapar(p.pregunta)}</td>
        <td><span class="pill cat">${escapar(nombreCat)}</span></td>
        <td class="cell-clip">${escapar(p.respuesta)}</td>
        <td class="row-actions">
          <button class="link-btn" onclick="editarPregunta(${p.id})">Editar</button>
          <button class="link-btn danger" onclick="eliminarPregunta(${p.id})">Eliminar</button>
        </td>
      </tr>`;
    })
    .join("");
}

$("pregunta-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const id = $("pregunta-id").value;
  const body = {
    categoria_id: parseInt($("pregunta-categoria").value, 10),
    pregunta: $("pregunta-texto").value,
    respuesta: $("pregunta-respuesta").value,
    palabras_clave: $("pregunta-claves").value,
  };
  try {
    if (id) {
      await api("PUT", `/preguntas/${id}`, body);
    } else {
      await api("POST", "/preguntas", body);
    }
    resetPreguntaForm();
    cargarPreguntas();
  } catch (error) {
    alert(error.message);
  }
});

function editarPregunta(id) {
  const p = preguntasCache.find((x) => x.id === id);
  if (!p) return;
  $("pregunta-id").value = p.id;
  $("pregunta-categoria").value = p.categoria_id;
  $("pregunta-texto").value = p.pregunta;
  $("pregunta-respuesta").value = p.respuesta;
  $("pregunta-claves").value = p.palabras_clave || "";
  $("pregunta-submit").textContent = "Guardar";
  $("pregunta-cancel").classList.remove("hidden");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

async function eliminarPregunta(id) {
  if (!confirm("¿Eliminar esta pregunta?")) return;
  try {
    await api("DELETE", `/preguntas/${id}`);
    cargarPreguntas();
  } catch (error) {
    alert(error.message);
  }
}

function resetPreguntaForm() {
  $("pregunta-id").value = "";
  $("pregunta-form").reset();
  $("pregunta-submit").textContent = "Agregar";
  $("pregunta-cancel").classList.add("hidden");
}

$("pregunta-cancel").addEventListener("click", resetPreguntaForm);

async function cargarConsultas() {
  const consultas = await api("GET", "/consultas");
  const tbody = $("consultas-table").querySelector("tbody");
  tbody.innerHTML = consultas
    .map((c) => {
      const fecha = new Date(c.created_at).toLocaleString();
      const usuario = c.telegram_username
        ? "@" + c.telegram_username
        : c.telegram_user_id || "—";
      const pill = c.respondida
        ? '<span class="pill yes">Sí</span>'
        : '<span class="pill no">No</span>';
      return `<tr>
        <td>${escapar(fecha)}</td>
        <td>${escapar(usuario)}</td>
        <td class="cell-clip">${escapar(c.consulta_texto)}</td>
        <td>${pill}</td>
      </tr>`;
    })
    .join("");
}

async function cargarConfiguracion() {
  try {
    const chat = await api("GET", "/configuracion/telegram_chat_id");
    $("config-chat").value = chat.valor || "";
  } catch (e) {}
  try {
    const mensaje = await api("GET", "/configuracion/mensaje_no_encontrado");
    $("config-mensaje").value = mensaje.valor || "";
  } catch (e) {}
}

$("config-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  $("config-status").textContent = "";
  try {
    await api("PUT", "/configuracion/telegram_chat_id", {
      valor: $("config-chat").value,
    });
    await api("PUT", "/configuracion/mensaje_no_encontrado", {
      valor: $("config-mensaje").value,
    });
    $("config-status").textContent = "Cambios guardados";
  } catch (error) {
    alert(error.message);
  }
});

if (token) {
  mostrarApp();
} else {
  mostrarLogin();
}
