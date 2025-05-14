# Imagen base
FROM python:3.13-slim

# Directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt .
COPY etl_to_mongo.py .
COPY eda_dataset.csv .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutar el script al iniciar el contenedor
CMD ["python", "salario.py"]
