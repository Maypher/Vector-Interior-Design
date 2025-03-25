#!/bin/sh

mkdir -p /var/nginx/logs/
touch /var/nginx/logs/error.log 
touch /var/nginx/logs/access.log 

envsubst '${ADMIN_FRONTEND_URL} ${USER_FRONTEND_URL} ${ADMIN_PORT} ${USER_PORT} ${USER_BACKEND_URL} ${ADMIN_BACKEND_URL} ${DEV_MODE}' < /etc/nginx/templates/nginx.conf > /etc/nginx/conf.d/default.conf
openresty -g 'daemon off;'
