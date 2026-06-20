"""Envio de reportes por correo (SMTP)."""
from __future__ import annotations

import smtplib
from email.message import EmailMessage

from app.core.config import settings

_MIME = {
    "pdf": ("application", "pdf"),
    "xlsx": ("application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
    "csv": ("text", "csv"),
}


class EmailService:
    def build_message(self, to: str, subject: str, body: str,
                      attachment: bytes, filename: str, fmt: str) -> EmailMessage:
        msg = EmailMessage()
        msg["From"] = settings.SMTP_FROM
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)
        maintype, subtype = _MIME.get(fmt, ("application", "octet-stream"))
        msg.add_attachment(attachment, maintype=maintype, subtype=subtype, filename=filename)
        return msg

    def send(self, to: str, subject: str, body: str,
             attachment: bytes, filename: str, fmt: str) -> str:
        if not settings.SMTP_HOST:
            raise RuntimeError("SMTP no configurado (definí SMTP_HOST en el .env)")
        msg = self.build_message(to, subject, body, attachment, filename, fmt)
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_TLS:
                server.starttls()
            if settings.SMTP_USER:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD or "")
            server.send_message(msg)
        return f"Reporte enviado a {to}"
