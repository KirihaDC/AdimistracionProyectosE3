# AdimistracionProyectosE3

Para correr el django en el programa hacer esto

# Instalar Django
pip install django

# Crear todo lo que se ocupa cada que se descarga una version nueva del git segun sea necesario
# Tambien arranca el codigo
docker-compose up 

# Arrancar docker
python manage.py runserver // Arrancar el proyecto



# Para la base de datos
# Instalar MariaDB en dado caso de ser necesario por algun tipo de error
docker pull mariadb

# Accede al contenedor de MariaDB:
docker exec -it Usuarios bash

# Conectarte al servidor
mysql -u root -p


CREATE TABLE IF NOT EXISTS Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(255) NOT NULL,
    correo VARCHAR(255) NOT NULL,
    contraseña VARCHAR(255) NOT NULL
);

INSERT INTO Usuarios (usuario, correo, contraseña) 
VALUES ('admin', 'kirihadc020@gmail.com', '123');
