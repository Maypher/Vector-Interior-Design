# Nginx

This is the main server that's exposed to the open internet. It works as a reverse proxy to all the different services the application offers.

In reality it uses [OpenResty](https://openresty.org/en/) due to the use of Lua to optimize and cache images but the name stays ¯\\_(ツ)_/¯.

It exposes the following servers:

- `${BACKEND_URL}`: This url is set as an environment variable (planned to be backend.vectorinterior.design) and it proxies to two different backends based on the `$origin` header. It proxies to [admin-backend](/backend/src/admin/) if the origin is `${ADMIN_FRONTEND_URL}` or to [user-frontend](/backend/src/user/) for all other origins. It has a 10mb body size limit to allow image uploads from the admin service.
  - `location: /images/<image>`: This url returns the image identified by filename in webp format. It gets optimized and cached by lua and on subsequent requests there's no need for reoptimazation. 
- `${ADMIN_FRONTEND_URL}`: The url is set as an environment variable (planned to be admin.vectorinterior.design) and it proxies to the [admin-frontend](/frontend/admin/).
- `${USER_FRONTEND_URL}`:  The url is set as an environment variable (planned to be vectorinterior.design) and it proxies to the [user-frontend](/frontend/user/). This is the main frontend all users will see.
- `PORT: 5174`: This url is only available when running with `DEV_MODE=1` and it exposes the user frontend in development.
    - `PORT: 5112`: The hmr port to allow vite's for hot module reloading while developing.
- `PORT: 5173`: This url is only available when running with `DEV_MODE=1` and it exposes the admin frontend in development.
  - `PORT: 5111:` The hmr port to allow vite's for hot module reloading while developing.
-  `PORT: 8080`: This url is only available when running with `DEV_MODE=1` and it exposes the admin backend directly.


**Note:** To correctly expose the correct ports during development use docker-compose's overwrite mechanism by doing `docker-compose --profile prod -f docker-compose.yml -f docker-compose.dev.yml`. This will expose all ports required for development.
