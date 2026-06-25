FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias primero (mejor cacheo de capas)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

EXPOSE 8000

# Servidor de producción ligero (uvicorn). Para producción real se podría
# usar gunicorn con workers uvicorn; para esta práctica uvicorn es suficiente.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
