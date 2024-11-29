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

--- 

> /obras/crear/

**Método**: POST

**Descripción**: Crea una nueva obra.

**Parámetros (form)**

- **json**:
```
{
    "name": string,
    "description": string,
    "alt_texts": [{
        "filename": string // Must match filename of uploaded file,
        "alt_text": string
    }, ...]
}
```
- **images**: `[png, jpeg, jpg]`
---
> /obras/borrar/id

**Método**: DELETE

**Descripción**: Borra la obra identificada por id junto a 
todas las imágenes vinculadas a esta.

**Parámetros**

- **id**: El id de la obra.

> /obras/actualizar/id

**Método**: PUT

**Descripción**: Actualiza la información de una obra

**Parámetros (form)**

- **json**:

```
{
    "obra_id": int,
    "name": string,
    "description": string,
    "images_delete": [string], // images filename to delete
    "images_change": [{
        "filename": string, // The name of the image to edit,
        "alt_text": string, // The new alt text (Optional).
        "index": int // The index to move the image to.
    }, ...],
    "images_new_info": {
        "filename": string, // The filename to associate the alt text
        "alt_text": string
    }
}
```
- **images_new**: `[png, jpg, jpeg]`

**Explicación**
Todos los valores son opcionales al menos que se especifique lo contrario.

- **obra_id**: El id de la obra.
- **name**: El nuevo nombre de la obra.
- **description**: La nueva descripción de la obra.
- **images_delete**: Nombres de imágenes a borrar.
-  **images_change**: Utilizado para cambiar el texto alternativo o la posición de una imagen.
- **images_new_info**: Información relacionada a cada nueva imagen. Requerido si hay nuevas imágenes y deben ser la misma cantidad.
- **images_new**: Nuevas imágenes que añadir. Debe ser la misma cantidad que `images_new_info`.



> /auth/usuario-creado

**Método**: GET

**Descripción**: Retorna la cantidad de usuarios creados.

> /auth/crear-cuenta

**Método**: POST

**Descripción**: Crea una nueva cuenta. Funciona únicamente si no hay usuarios creados.

**Parámetros**:

- **email**: Correo electrónico.
- **name**: Nombre de usuario.
- **password**: Contraseña.

> /auth/iniciar-sesion

**Método**: POST

**Descripción**: Inicia sesión con un usuario ya creado.

**Parámetros**:

- **email**: Correo electrónico.
- **password**: Contraseña.

> /auth/cerrar-sesion

**Método**: POST

**Descripción**: Cierra la sesión del actual usuario.

> /auth/info-usuario

**Método**: GET

**Descripción**: Retorna la información del usuario con la sesión iniciada en el formato `{id: int, name: str, email: str}`.
