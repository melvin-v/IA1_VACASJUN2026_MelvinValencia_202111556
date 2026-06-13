"""Servicio de notificacion por Telegram.

Envia el resultado de un diagnostico a un chat de Telegram usando la Bot API
(metodo sendMessage). El envio se hace en un hilo en segundo plano para no
bloquear la respuesta de la API, y cualquier fallo se registra sin afectar
el diagnostico que ya se le devolvio al usuario.
"""

import html
import logging
import threading

import httpx

from app.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from app.schemas.diagnostico_schema import DiagnosticoResponse

logger = logging.getLogger("doctor_byte.telegram")

_API_URL = "https://api.telegram.org/bot{token}/sendMessage"


class TelegramNotifier:
    def __init__(self, token: str = TELEGRAM_BOT_TOKEN, chat_id: str = TELEGRAM_CHAT_ID):
        self._token = token
        self._chat_id = chat_id

    def esta_configurado(self) -> bool:
        """True solo si hay token y chat_id; si no, las notificaciones se omiten."""
        return bool(self._token and self._chat_id)

    def enviar_diagnostico(self, respuesta: DiagnosticoResponse) -> None:
        """Dispara el envio del diagnostico en segundo plano (no bloquea)."""
        if not self.esta_configurado():
            logger.info("Telegram no configurado; se omite la notificacion.")
            return
        texto = self._formatear(respuesta)
        hilo = threading.Thread(target=self._enviar, args=(texto,), daemon=True)
        hilo.start()

    def _enviar(self, texto: str) -> None:
        url = _API_URL.format(token=self._token)
        try:
            r = httpx.post(
                url,
                json={"chat_id": self._chat_id, "text": texto, "parse_mode": "HTML"},
                timeout=10,
            )
            if r.status_code != 200:
                logger.warning("Telegram respondio %s: %s", r.status_code, r.text)
        except Exception as e:  # noqa: BLE001 - no debe romper el diagnostico
            logger.warning("No se pudo enviar a Telegram: %s", e)

    @staticmethod
    def _formatear(respuesta: DiagnosticoResponse) -> str:
        """Arma el mensaje en HTML (escapando el contenido dinamico)."""
        esc = html.escape
        sintomas = ", ".join(esc(s) for s in respuesta.sintomas_evaluados)

        lineas = [
            "\U0001FA7A <b>Doctor Byte - Nuevo diagnostico</b>",
            "",
            f"<b>Sintomas evaluados:</b> {sintomas}",
            "",
        ]

        if respuesta.fallas:
            lineas.append(f"\u26A0\uFE0F <b>{esc(respuesta.mensaje)}</b>")
            lineas.append("")
            for f in respuesta.fallas:
                lineas.append(f"\u2022 <b>{esc(f.descripcion)}</b>")
                lineas.append(f"   <i>Recomendacion:</i> {esc(f.recomendacion)}")
        else:
            lineas.append(f"\u2705 {esc(respuesta.mensaje)}")

        return "\n".join(lineas)
