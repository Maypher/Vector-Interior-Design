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

> /

**Método**: GET

**Descripción**: Retorna todas las obras públicas paginadas.

**Parámetros (URL ?=)**

- **name**: str = Filtrar búsqueda por nombre.
- **page**: int = Página de obras que retornar.
- **page_size**: int = Tamaño de cada página.


> /id

**Método**: GET

**Descripción**: Retorna la información de una obra dado su id si es pública.

**Parámetros**

- **id**: El id de la obra que retornar.

## Admin

--- 

### Obras

Una obra es la clase principal del programa. Contiene ambientes e imágenes.

> /obras/

**Método**: GET

**Descripción**: Retorna todas las obras paginadas.

**Parámetros (URL ?=)**

- **name**: str = Filtrar búsqueda por nombre.
- **page**: int = Página de obras que retornar.
- **page_size**: int =Tamaño de cada página.


> /obras/id

**Método**: GET

**Descripción**: Retorna la información de una obra dado su id.

**Parámetros**

- **id**: El id de la obra que retornar.

> /obras/crear/

**Método**: POST

**Descripción**: Crea una nueva obra.

**Parámetros (form)**

- **name (str)**: El nombre de la obra.
- **Descripción (str)**: La descripción de la obra.
---
> /obras/borrar/id

**Método**: DELETE

**Descripción**: Borra la obra identificada por id junto a 
todos los ambientes e imágenes vinculadas a esta.

**Parámetros**

- **id**: El id de la obra.

> /obras/actualizar/id

**Método**: PUT

**Descripción**: Actualiza la información de una obra.

**Parámetros (form)**

- **name (str)**: El nuevo nombre de la obra.
- **description (str)**: La nueva descripción de la obra.
- **thumbnail (str) (optional)**: La imagen principal que aparecerá en la miniatura de la obra.
- **index**: El nuevo índice (zero based) para esta obra. Utilizado para mostrarlo en la UI.
- **public (bool)**: Establece si una obra puede ser vista por el público. 

### Ambientes

Un ambiente es una sección de una obra. Esta contiene imágenes.

> /ambientes/crear

**Método**: POST

**Descripción**: Crea un nuevo ambiente.

**Parámetros (form)**

- **obra_id (int)**: El ID de la obra a la que vincular este ambiente.
- **Nombre (str)**: El nombre de este ambiente. Dos ambientes no pueden tener el mismo nombre en una misma obra.
- **Descripción (str) (opcional)**: La descripción del ambiente.

> /ambientes/borrar/id

**Método**: DELETE

**Descripción**: Borra el ambiente identificado por ID junto a todas las imágenes asociadas a este.

**Parámetros (form)**

- **id**: El ID del ambiente para borrar.

> /ambientes/actualizar/id

**Método**: PUT

**Descripción**: Actualiza la información de un ambiente.

**Parámetros (form)**:

- **name (str)**: El nuevo nombre del ambiente.
- **description (str)**: La nueva descripción del ambiente.
- **index (int)**: El nuevo indice del ambiente (zero-based). Utilizado para ordenarlos en la UI.

**Explicación**: Todos los valores son opcionales.

### Imágenes

Una imagen. Contiene un texto alternativo.

> /imagenes/crear

**Método**: POST

**Descripción**: Crea una nueva imagen.

**Parámetros (form)**

- **ambiente_id (int)**: El ID del ambiente a la que vincular esta imagen.
- **alt_text (str)**: El texto alternativo de esta imagen.
- **Descripción (str) (opcional)**: La descripción del ambiente.

> /imagenes/borrar/filename

**Método**: DELETE

**Descripción**: Borra la imagen identificado por filename.

**Parámetros (form)**

- **filename**: El nombre de la imagen que borrar.

> /imagenes/actualizar/id

**Método**: PUT

**Descripción**: Actualiza la información de una imagen.

**Parámetros (form)**:

- **alt_text (str)**: El nuevo texto alternativo de la imagen.
- **index (int)**: El nuevo indice de la imagen (zero-based). Utilizado para ordenarlos en la UI.

**Explicación**: Todos los valores son opcionales.
****

### Autenticación

**Explicación**
Todos los valores son opcionales.

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
