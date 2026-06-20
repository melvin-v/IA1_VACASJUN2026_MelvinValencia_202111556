const API = "/api/v1";
let token = localStorage.getItem("si_token") || null;

const $ = (s) => document.querySelector(s);
const el = (s) => document.querySelector(s);

// ---------- helpers de API ----------
async function api(path, { method = "GET", body, form, auth = true } = {}) {
  const headers = {};
  if (auth && token) headers["Authorization"] = `Bearer ${token}`;
  let payload;
  if (form) payload = form;
  else if (body) { headers["Content-Type"] = "application/json"; payload = JSON.stringify(body); }
  const r = await fetch(API + path, { method, headers, body: payload });
  if (r.status === 401) { logout(); throw new Error("Sesión expirada"); }
  const txt = await r.text();
  const data = txt ? JSON.parse(txt) : null;
  if (!r.ok) throw new Error(data?.detail || "Error en la solicitud");
  return data;
}

// ---------- auth ----------
async function login() {
  el("#login-error").textContent = "";
  const email = el("#login-email").value.trim();
  const pass = el("#login-password").value;
  try {
    const form = new URLSearchParams({ username: email, password: pass });
    const r = await fetch(`${API}/auth/login`, { method: "POST", body: form });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || "Credenciales inválidas");
    token = data.access_token;
    localStorage.setItem("si_token", token);
    await enterApp();
  } catch (e) { el("#login-error").textContent = e.message; }
}

async function register() {
  el("#login-error").textContent = "";
  const email = el("#login-email").value.trim();
  const pass = el("#login-password").value;
  try {
    await api("/auth/register", { method: "POST", auth: false,
      body: { email, full_name: email.split("@")[0], password: pass } });
    await login();
  } catch (e) { el("#login-error").textContent = e.message; }
}

function logout() {
  token = null; localStorage.removeItem("si_token");
  el("#app-view").hidden = true; el("#login-view").hidden = false;
}

async function enterApp() {
  const me = await api("/users/me");
  el("#user-label").textContent = me.email;
  el("#login-view").hidden = true; el("#app-view").hidden = false;
  showTab("upload");
}

// ---------- navegación ----------
function showTab(name) {
  document.querySelectorAll(".nav-item").forEach(b => b.classList.toggle("active", b.dataset.tab === name));
  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  el(`#tab-${name}`).classList.add("active");
  if (name === "invoices") loadInvoices();
  if (name === "providers") loadProviders();
  if (name === "logs") loadLogs();
}

// ---------- subir factura ----------
let selectedFile = null;
function pickFile(f) {
  selectedFile = f; el("#file-name").textContent = f ? f.name : "";
  el("#btn-upload").disabled = !f;
}
async function uploadInvoice() {
  if (!selectedFile) return;
  el("#btn-upload").disabled = true; el("#btn-upload").textContent = "Procesando…";
  const fd = new FormData(); fd.append("file", selectedFile);
  try {
    const inv = await api("/invoices/upload", { method: "POST", form: fd });
    const box = el("#upload-result"); box.hidden = false;
    box.innerHTML = `<b>Factura procesada</b> <span class="pill ${inv.status}">${inv.status}</span>
      <div class="result-grid">
        <div>Número: <b>${inv.invoice_number || "—"}</b></div>
        <div>Fecha: <b>${inv.invoice_date || "—"}</b></div>
        <div>Proveedor: <b>${inv.provider_name || "—"}</b></div>
        <div>NIT: <b>${inv.nit || "—"}</b></div>
        <div>Subtotal: <b>${inv.subtotal ?? "—"}</b></div>
        <div>Impuestos: <b>${inv.taxes ?? "—"}</b></div>
        <div>Total: <b>${inv.total ?? "—"}</b></div>
      </div>`;
  } catch (e) {
    const box = el("#upload-result"); box.hidden = false;
    box.innerHTML = `<span class="error-msg">${e.message}</span>`;
  } finally {
    el("#btn-upload").textContent = "Procesar"; el("#btn-upload").disabled = false;
    pickFile(null);
  }
}

// ---------- facturas ----------
async function loadInvoices() {
  const status = el("#status-filter").value;
  const q = status ? `?status_filter=${status}` : "";
  const rows = await api(`/invoices${q}`);
  const t = el("#invoices-table");
  if (!rows.length) { t.innerHTML = "<p class='muted'>Sin facturas.</p>"; return; }
  t.innerHTML = `<table><thead><tr>
    <th>#</th><th>Número</th><th>Proveedor</th><th>NIT</th><th>Total</th><th>Estado</th><th></th>
    </tr></thead><tbody>${rows.map(i => `<tr>
      <td>${i.id}</td><td>${i.invoice_number || "—"}</td><td>${i.provider_name || "—"}</td>
      <td>${i.nit || "—"}</td><td class="num">${i.total ?? "—"}</td>
      <td><span class="pill ${i.status}">${i.status}</span></td>
      <td><button class="btn btn-ghost btn-sm" onclick="runRpa(${i.id},this)">RPA</button></td>
    </tr>`).join("")}</tbody></table>`;
}
async function runRpa(id, btn) {
  btn.disabled = true; btn.textContent = "…";
  try { const r = await api(`/invoices/${id}/rpa`, { method: "POST" }); btn.textContent = "✓ " + r.message.slice(0, 12); }
  catch (e) { btn.textContent = "✗"; alert(e.message); }
}

// ---------- proveedores ----------
async function loadProviders() {
  const rows = await api("/providers");
  const t = el("#providers-table");
  t.innerHTML = rows.length ? `<table><thead><tr>
    <th>#</th><th>Nombre</th><th>NIT</th><th>Correo</th><th></th></tr></thead><tbody>
    ${rows.map(p => `<tr><td>${p.id}</td><td>${p.name}</td><td>${p.nit}</td>
      <td>${p.email || "—"}</td>
      <td><button class="btn btn-ghost btn-sm" onclick="delProvider(${p.id})">Borrar</button></td>
    </tr>`).join("")}</tbody></table>` : "<p class='muted'>Sin proveedores.</p>";
}
async function addProvider() {
  el("#provider-error").textContent = "";
  try {
    await api("/providers", { method: "POST", body: {
      name: el("#prov-name").value.trim(), nit: el("#prov-nit").value.trim(),
      email: el("#prov-email").value.trim() || null } });
    el("#prov-name").value = el("#prov-nit").value = el("#prov-email").value = "";
    loadProviders();
  } catch (e) { el("#provider-error").textContent = e.message; }
}
async function delProvider(id) {
  if (!confirm("¿Borrar proveedor?")) return;
  await api(`/providers/${id}`, { method: "DELETE" }); loadProviders();
}

// ---------- bitácora ----------
async function loadLogs() {
  const rows = await api("/logs");
  const t = el("#logs-table");
  t.innerHTML = rows.length ? `<table><thead><tr>
    <th>#</th><th>Documento</th><th>Estado</th><th>Resultado</th><th>Fecha</th></tr></thead><tbody>
    ${rows.map(l => `<tr><td>${l.id}</td><td>${l.document_name || "—"}</td>
      <td><span class="pill ${l.status}">${l.status}</span></td><td>${l.result || "—"}</td>
      <td>${(l.processed_at || "").replace("T", " ").slice(0, 16)}</td></tr>`).join("")}
    </tbody></table>` : "<p class='muted'>Bitácora vacía.</p>";
}

// ---------- reportes ----------
async function downloadReport(fmt) {
  const r = await fetch(`${API}/reports/invoices?format=${fmt}`, {
    headers: { Authorization: `Bearer ${token}` } });
  const blob = await r.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = `reporte_facturas.${fmt}`; a.click();
  URL.revokeObjectURL(url);
}
async function emailReport() {
  el("#report-msg").textContent = "";
  const to = el("#email-to").value.trim(); const fmt = el("#email-format").value;
  try {
    const r = await api(`/reports/invoices/email?to=${encodeURIComponent(to)}&format=${fmt}`, { method: "POST" });
    el("#report-msg").textContent = r.message;
  } catch (e) { el("#report-msg").textContent = e.message; el("#report-msg").className = "error-msg"; }
}

// ---------- eventos ----------
el("#btn-login").onclick = login;
el("#btn-register").onclick = register;
el("#btn-logout").onclick = logout;
el("#login-password").addEventListener("keydown", e => { if (e.key === "Enter") login(); });
document.querySelectorAll(".nav-item").forEach(b => b.onclick = () => showTab(b.dataset.tab));
el("#btn-browse").onclick = () => el("#file-input").click();
el("#file-input").onchange = e => pickFile(e.target.files[0]);
el("#btn-upload").onclick = uploadInvoice;
el("#status-filter").onchange = loadInvoices;
el("#btn-add-provider").onclick = addProvider;
el("#btn-email").onclick = emailReport;
document.querySelectorAll("[data-report]").forEach(b => b.onclick = () => downloadReport(b.dataset.report));
const dz = el("#dropzone");
["dragover", "dragenter"].forEach(ev => dz.addEventListener(ev, e => { e.preventDefault(); dz.classList.add("drag"); }));
["dragleave", "drop"].forEach(ev => dz.addEventListener(ev, e => { e.preventDefault(); dz.classList.remove("drag"); }));
dz.addEventListener("drop", e => pickFile(e.dataTransfer.files[0]));

// ---------- arranque ----------
if (token) enterApp().catch(logout);
