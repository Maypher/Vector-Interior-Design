# Admin Backend

This is the admin backend of the Vector: Interior Design website. It uses a Sanic server and connects to the [postgresql database](/database/) using psycopg. The following routes are available in this backend.

- `/auth/iniciar-sesion`: Used to login into the admin panel. By passing an email and password a user session is created and a session id is set in an http-only cookie.
- `/auth/cerrar-sesion`: Used to logout. Removes session and deletes session id cookie.
- `/auth/info-usuario`: Used to get the info from the currently logged in user.
- `/graphql`: Gives access to the graphql API. The docs for this API are located [here](/backend/src/admin/docs/index.html).

# User management

Users can be managed using the [cli tool](./cli/users.py). The available commands are the following:

- `new --name || -n NAME --email || -e EMAIL --password || -p PASSWORD`: Used to create a new user identified by the given credentials
- `delete EMAIL`: Deletes the user identified by the given email.
- `change_password --email || -e EMAIL --password || -p PASSWORD`: Changes the password for the user identified by EMAIL to PASSWORD.


# Database management

All migrations are in its [respective folder](./migrations/). To keep the database up to date there's a [CLI tool](./cli/migrations.py) that exposes the following functionality:

- `new FILENAME`: Creates a new migration sql file and its corresponding down migration. **MUST BE USED IN DEVELOPMENT. RUNNING THIS IN PRODUCTION WILL ACCOMPLISH NOTHING**.
- `migrate --version NUMBER --directory`: Migrates the database upwards to the specified migration or to the latest one if no version was specified. `--directory` specifies the folder where migrations are stored.
- `rollback --version NUMBER`: Rolls back all migrations down to version number. `NUMBER` is not applied so the last migration removed is `ROLLBACK + 1`.
