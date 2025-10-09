# Imagen base ligera con Python 3.11
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar dependencias y luego instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copia el codigo del microservicio
COPY . .

# Exponer el puerto donde correrá FastAPI
EXPOSE 8084

# Comando para iniciar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8084"]
