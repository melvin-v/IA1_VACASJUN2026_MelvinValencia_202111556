from enum import Enum


class InvoiceStatus(str, Enum):
    """Estados posibles de una factura / registro de bitácora."""
    PENDIENTE = "PENDIENTE"
    PROCESADO = "PROCESADO"
    ERROR = "ERROR"
    RECHAZADO = "RECHAZADO"
