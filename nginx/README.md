# Nginx

This is the main server that's exposed to the open internet. It works as a reverse proxy to all the different services the application offers.

In reality it uses [OpenResty](https://openresty.org/en/) due to the use of Lua to optimize and cache images but the name stays ¯\\_(ツ)_/¯.

It exposes the following servers:

- `${USER_URL}`: The url for user frontend (planned to be vectorinterior.design). This is the main page users will use and it will proxy to [user-frontend](/frontend/user/).
  - `location: /images/<image>`: This url returns the image identified by filename in webp format. It gets optimized and cached by lua and on subsequent requests there's no need for reoptimazation. 
  - - `location: ${USER_API_PATH}`: The path to access the [user-backend](/backend/src/user/).
- `${ADMIN_URL}`: The url is set as an environment variable (planned to be admin.vectorinterior.design) and it proxies to the [admin-frontend](/frontend/admin/).
  - `location: /images/<image>`: Same as `USER_URL` location.
  - `location: ${USER_API_PATH}`: The path to access the [admin-backend](/backend/src/admin/). 
- `PORT: 5174`: This url is only available when running with `DEV_MODE=1` and it exposes the user frontend in development.
    - `PORT: 5112`: The hmr port to allow vite's for hot module reloading while developing.
- `PORT: 5173`: This url is only available when running with `DEV_MODE=1` and it exposes the admin frontend in development.
  - `PORT: 5111:` The hmr port to allow vite's for hot module reloading while developing.


**Note:** To correctly expose the correct ports during development use docker-compose's overwrite mechanism by doing `docker-compose --profile prod -f docker-compose.yml -f docker-compose.dev.yml`. This will expose all ports required for development.
