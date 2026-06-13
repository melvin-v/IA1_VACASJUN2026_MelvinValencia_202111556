"""Obtiene el chat_id para configurar las notificaciones.

Pasos:
  1. Crea el bot con @BotFather y copia el token en tu archivo .env
     (variable TELEGRAM_BOT_TOKEN).
  2. Abri Telegram, busca tu bot y enviale cualquier mensaje (ej: "hola").
  3. Ejecuta este script:  python obtener_chat_id.py
  4. Copia el chat_id que aparece en TELEGRAM_CHAT_ID dentro de tu .env
"""

import sys

import httpx

from app.config import TELEGRAM_BOT_TOKEN

if not TELEGRAM_BOT_TOKEN:
    print("Falta TELEGRAM_BOT_TOKEN en el archivo .env")
    sys.exit(1)

url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
r = httpx.get(url, timeout=10)
data = r.json()

if not data.get("ok"):
    print("Error al consultar Telegram:", data)
    sys.exit(1)

updates = data.get("result", [])
if not updates:
    print("No hay mensajes todavia. Enviale un mensaje a tu bot y volve a correr este script.")
    sys.exit(0)

print("Chats encontrados:")
vistos = set()
for u in updates:
    chat = (u.get("message") or u.get("edited_message") or {}).get("chat")
    if chat and chat["id"] not in vistos:
        vistos.add(chat["id"])
        nombre = chat.get("title") or chat.get("username") or chat.get("first_name", "")
        print(f"  chat_id = {chat['id']}   ({nombre})")
