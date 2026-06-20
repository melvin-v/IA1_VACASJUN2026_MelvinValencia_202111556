"""Modulo de Computer Vision + OCR.

Flujo: cargar archivo (imagen o PDF) -> preprocesar con OpenCV ->
extraer texto con Tesseract. Todo el procesamiento es local (sin IA externa).
"""
from __future__ import annotations

import os
from typing import List

import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path

from app.core.config import settings

if settings.TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD


class OCRService:
    # ---------- carga ----------
    def _load_images(self, file_path: str) -> List[np.ndarray]:
        ext = os.path.splitext(file_path)[1].lower().lstrip(".")
        if ext == "pdf":
            pages = convert_from_path(file_path, dpi=settings.PDF_DPI)
            return [cv2.cvtColor(np.array(p), cv2.COLOR_RGB2BGR) for p in pages]
        img = cv2.imread(file_path)
        return [img] if img is not None else []

    # ---------- Computer Vision: preprocesamiento ----------
    def _deskew(self, gray: np.ndarray) -> np.ndarray:
        """Corrige la inclinacion del documento usando el angulo del texto."""
        inv = cv2.bitwise_not(gray)
        coords = np.column_stack(np.where(inv > 0))
        if coords.shape[0] < 50:
            return gray
        angle = cv2.minAreaRect(coords)[-1]
        angle = -(90 + angle) if angle < -45 else -angle
        if abs(angle) < 0.5:
            return gray
        h, w = gray.shape
        m = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
        return cv2.warpAffine(gray, m, (w, h),
                              flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    def preprocess(self, img: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = self._deskew(gray)
        gray = cv2.medianBlur(gray, 3)                       # quita ruido
        _, thresh = cv2.threshold(                            # binarizacion Otsu
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        return thresh

    # ---------- OCR ----------
    def extract_text(self, file_path: str) -> str:
        images = self._load_images(file_path)
        if not images:
            raise ValueError("No se pudo leer el archivo (formato o ruta invalida)")
        partes = []
        for img in images:
            pre = self.preprocess(img)
            partes.append(pytesseract.image_to_string(pre, lang=settings.TESSERACT_LANG))
        return "\n".join(partes).strip()
