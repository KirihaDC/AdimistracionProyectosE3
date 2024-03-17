# Sistema de Presentaciones

## Descripción

El Sistema de Presentaciones es una herramienta web diseñada para crear, visualizar y navegar presentaciones de manera eficiente y efectiva. Basado en una estructura de archivos TXT, el sistema facilita a los administradores la creación de contenido dinámico que los usuarios pueden explorar utilizando tanto teclado como mouse.

## Características Principales

- **Creación de Presentaciones**: Importa y configura presentaciones a partir de archivos TXT.
- **Navegación Interactiva**: Soporte completo para navegación de presentaciones con teclado y mouse.
- **Autenticación de Usuarios**: Sistema de login para administradores con seguridad integrada.
- **Diseño Intuitivo**: Interfaz de usuario diseñada con HTML para una experiencia de usuario mejorada.
- **Gestión de Datos Robusta**: Usa MariaDB para un almacenamiento de datos eficiente y seguro.

## Tecnologías Utilizadas

- **Django**: Un framework web de alto nivel en Python que fomenta el desarrollo rápido y un diseño limpio y pragmático.
- **Python**: Lenguaje de programación que permite trabajar rápidamente e integrar sistemas de manera eficiente.
- **Docker**: Plataforma de contenedores que permite empaquetar una aplicación y sus dependencias en un contenedor virtual que puede ejecutarse en cualquier sistema Linux.
- **MariaDB**: Sistema de gestión de bases de datos relacional, derivado de MySQL, que se destaca por ser de código abierto y tener un rendimiento alto.
- **HTML**: Lenguaje de marcado utilizado para la creación de páginas web y aplicaciones web. En este proyecto, HTML se utiliza para diseñar la interfaz de usuario.


## Configuración y Despliegue

### Clonar el Repositorio

```bash
git clone https://example.com/your-project.git
cd your-project
```
## Configurar Variables de Entorno
Copia .env.example a .env y ajusta las variables según necesites:
```
cp .env.example .env
```
### Construir y Ejecutar con Docker Compose
Utiliza Docker Compose para levantar todos los servicios:
```
docker-compose up --build

```
### Migraciones y Superusuario
Realiza las migraciones iniciales y crea un superusuario para Django:

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```
## Acceso a la Aplicación
La aplicación estará disponible en http://localhost:8000. Navega a esta dirección para comenzar a usar el sistema de presentaciones.

## Contacto

Para soporte, puedes contactar a ... o abrir un issue en este repositorio.