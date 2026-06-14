import os
import time

import httpx

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
API_URL = os.getenv("API_URL", "http://api:8000")
BOT_API_KEY = os.getenv("BOT_API_KEY", "cambia-esta-clave-interna-del-bot")

TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"
POLL_TIMEOUT = 30

BIENVENIDA = (
    "Hola, soy SmartBot, el asistente de la Escuela de Vacaciones.\n\n"
    "Escríbeme tu duda sobre asignación, notas, pagos, reembolsos o la "
    "modalidad del curso y te responderé con la información del normativo.\n\n"
    "Usa /ayuda para ver ejemplos."
)

AYUDA = (
    "Puedes preguntarme cosas como:\n"
    "- ¿Cuál es la nota mínima para aprobar?\n"
    "- ¿Cuánto cuesta un curso de 2 horas?\n"
    "- ¿Hay becas o descuentos?\n"
    "- ¿Cuándo aplica un reembolso?\n"
    "- ¿En qué modalidad se imparten las clases?"
)


def get_updates(client, offset):
    response = client.get(
        f"{TELEGRAM_API}/getUpdates",
        params={"offset": offset, "timeout": POLL_TIMEOUT},
    )
    response.raise_for_status()
    return response.json().get("result", [])


def send_message(client, chat_id, texto):
    client.post(
        f"{TELEGRAM_API}/sendMessage",
        json={"chat_id": chat_id, "text": texto},
    )


def consultar_api(client, texto, telegram_user_id, telegram_username):
    response = client.post(
        f"{API_URL}/bot/consultar",
        headers={"X-API-Key": BOT_API_KEY},
        json={
            "texto": texto,
            "telegram_user_id": telegram_user_id,
            "telegram_username": telegram_username,
        },
    )
    response.raise_for_status()
    return response.json()


def procesar_mensaje(client, mensaje):
    chat_id = mensaje.get("chat", {}).get("id")
    texto = mensaje.get("text", "")
    usuario = mensaje.get("from", {})

    if not chat_id or not texto:
        return

    if texto.startswith("/start"):
        send_message(client, chat_id, BIENVENIDA)
        return

    if texto.startswith("/ayuda") or texto.startswith("/help"):
        send_message(client, chat_id, AYUDA)
        return

    try:
        data = consultar_api(
            client, texto, usuario.get("id"), usuario.get("username")
        )
        send_message(client, chat_id, data["respuesta"])
    except Exception as error:
        print("Error al consultar la API:", error)
        send_message(
            client,
            chat_id,
            "Ocurrió un error procesando tu consulta. Intenta de nuevo más tarde.",
        )


def main():
    if not TOKEN:
        raise RuntimeError("Falta la variable de entorno TELEGRAM_BOT_TOKEN")

    offset = 0
    with httpx.Client(timeout=POLL_TIMEOUT + 10) as client:
        print("SmartBot iniciado. Esperando mensajes...")
        while True:
            try:
                for update in get_updates(client, offset):
                    offset = update["update_id"] + 1
                    mensaje = update.get("message")
                    if mensaje:
                        procesar_mensaje(client, mensaje)
            except Exception as error:
                print("Error en el bucle principal:", error)
                time.sleep(3)


if __name__ == "__main__":
    main()
