#!/bin/sh

mkdir -p /var/nginx/logs/;
touch /var/nginx/logs/error.log;
touch /var/nginx/logs/access.log;

nginx_secret=$(xargs </run/secrets/nginx_forward_secret);

export NGINX_SECRET="$nginx_secret";

envsubst '${ADMIN_URL} ${ADMIN_IMAGES_PATH} ${ADMIN_API_PATH} ${USER_URL} ${USER_IMAGES_PATH} ${USER_API_PATH} ${DEV_MODE} ${NGINX_SECRET}' < /etc/nginx/templates/nginx.conf > /etc/nginx/conf.d/default.conf;
openresty -g 'daemon off;'
