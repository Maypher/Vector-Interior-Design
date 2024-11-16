# TQ Portafolio

# Estructura

Utiliza Docker para contenerizar cada servicio. 
Los servicios son los siguientes:

- **Database:** Base de dato Postgresql.
- **Admin-backend**: El backend en python para administrar todas las obras y recursos de la página.
- **User-backend**: El backend en python para acceder a los recursos desde el frontend de usuario.
- **Nginx**: Reverse Proxy para redireccionar el tráfico y enviar archivos estáticos.
- **Admin/User-frontend**: El frontend escrito en Svelte. 
Todavía no estoy seguro de si incluirlo en el container de 
nginx o que tengan su propio container ya que son archivos estáticos.

# Variables de Entorno

- BUILD_TARGET: Blanco para el que construir (dev o prod)
- DATABASE_NAME: Nombre de la base de datos.
- POSTGRES_PASSWORD: Contraseña para el root user durante la creación de la base de datos.
- DATABASE_PORT: Puerto en el que exponer la base de datos.
- ADMIN_PORT: Puerto en el que exponer el admin backend.
- ADMIN_USERNAME: Nombre de usuario para el usuario de admin en la base de datos.
- ADMIN_PASSWORD: Contraseña para el usuario admin en la base de datos.
- USER_PORT: Puerto en el que exponer el backend del usuario en la base de datos.
- USER_USERNAME: Nombre de usuario para el user backend en la base de datos.
- USER_PASSWORD: Contraseña para el user backend en la base de datos.
