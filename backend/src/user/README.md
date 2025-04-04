# User Backend

This is the user backend for the Vector: Interior Design website. this is the server most users will be using. It uses a Sanic server with psycopg to connect to the [database](/database/). It only exposes one route:

- `/graphql/`: Exposes the graphql API. The docs can be found [here](/backend/src/admin/docs/index.html)
