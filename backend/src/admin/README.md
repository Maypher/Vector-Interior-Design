# Admin Backend

This is the admin backend of the Vector: Interior Design website. It uses a Sanic server and connects to the [postgresql database](/database/) using psycopg. The following routes are available in this backend.

- `/auth/iniciar-sesion`: Used to login into the admin panel. By passing an email and password a user session is created and a session id is set in an http-only cookie.
- `/auth/cerrar-sesion`: Used to logout. Removes session and deletes session id cookie.
- `/auth/info-usuario`: Used to get the info from the currently logged in user.
- `/graphql`: Gives access to the graphql API. The docs for this API are located [here](/backend/src/admin/docs/index.html).
