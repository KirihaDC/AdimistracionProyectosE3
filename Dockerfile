# Usa una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo en la imagen
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo en la imagen
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip3 install -r /app/requirements.txt

# Copia el resto de la aplicación al directorio de trabajo en la imagen
COPY . .

# Expone el puerto en el que la aplicación va a correr
EXPOSE 8000

# Comando para iniciar la aplicación Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
