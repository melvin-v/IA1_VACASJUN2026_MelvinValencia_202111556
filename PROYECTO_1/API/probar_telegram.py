import sys

import httpx

from app.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

if not (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID):
    print("Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID en el archivo .env")
    sys.exit(1)

url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
r = httpx.post(
    url,
    json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": "Doctor Byte esta conectado a Telegram correctamente.",
    },
    timeout=10,
)

print("status:", r.status_code)
print(r.json())
if r.status_code == 200:
    print("\nListo. Revisa el chat de Telegram, deberias ver el mensaje de prueba.")
