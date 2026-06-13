"""Configuracion de la aplicacion.

Lee variables de entorno (y un archivo .env si existe) para mantener los
secretos fuera del codigo. Crea tu propio .env a partir de .env.example.
"""

import os

from dotenv import load_dotenv

load_dotenv()  # carga el archivo .env si esta presente

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()
