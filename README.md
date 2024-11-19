# TQ Portafolio

# Estructura

Utiliza Docker para dividir cada servicio. 
Los servicios son los siguientes:

- **Database:** Base de dato Postgresql.
- **Admin-backend**: El backend en python para administrar todas las obras y recursos de la página.
- **User-backend**: El backend en python para acceder a los recursos desde el frontend de usuario.
- **Nginx**: Reverse Proxy para redirection del tráfico y enviar archivos estáticos.
- **Admin/User-frontend**: El frontend escrito en Svelte y será desplegado en Cloudflare.

# Variables de Entorno

- BUILD_TARGET: Blanco para el que construir (dev o prod)
- DATABASE_NAME: Nombre de la base de datos.
- POSTGRES_PASSWORD: Contraseña para el root user durante la creación de la base de datos.
- DATABASE_PORT: Puerto en el que exponer la base de datos.
- ADMIN_PORT: Puerto en el que exponer el admin backend.
- ADMIN_USERNAME: Nombre de usuario para el usuario de admin en la base de datos.
- ADMIN_PASSWORD: Contraseña para el usuario admin en la base de datos.
- ADMIN_SERVER_SECRET_KEY: Clave par encriptar el admin-backend.
- USER_PORT: Puerto en el que exponer el backend del usuario en la base de datos.
- USER_USERNAME: Nombre de usuario para el user backend en la base de datos.
- USER_PASSWORD: Contraseña para el user backend en la base de datos.

# Rutas

## Usuario

> /obras/

**Método**: GET

**Descripción**: Retorna todas las obras paginadas.

**Parámetros**

- **pagina**: int = Página de obras que retornar.
- **nombre**: str = Filtrar búsqueda por nombre.

--- 

> /obras/id

**Método**: GET

**Descripción**: Retorna la información de una obra dado su id.

**Parámetros**

- id: El id de la obra que retornar.

## Admin

> /obras/

**Método**: GET

**Descripción**: Retorna todas las obras paginadas.

**Parámetros**

- **pagina**: int = Página de obras que retornar.
- **nombre**: str = Filtrar búsqueda por nombre.

--- 

> /obras/id

**Método**: GET

**Descripción**: Retorna la información de una obra dado su id.

**Parámetros**

- id: El id de la obra que retornar.

> /obras/crear/

**Método**: POST

**Descripción**: Crea una nueva obra.

**Parámetros**

- **name**: El nombre de la obra.
- **description**: La descripción de la obra.
- **images[]**: Lista de imágenes relacionadas a la obra.
- **alt_text[]**: Lista de texto alternativo para cada imagen. 

> /obras/borrar/id

**Método**: DELETE

**Descripción**: Borra la obra identificada por id junto a 
todas las imágenes vinculadas a esta.

**Parámetros**

- **id**: El id de la obra.
