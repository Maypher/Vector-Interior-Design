#!/bin/sh

mkdir -p /var/nginx/logs/;
touch /var/nginx/logs/error.log;
touch /var/nginx/logs/access.log;

nginx_secret=$(xargs </run/secrets/nginx_forward_secret);

export NGINX_SECRET="$nginx_secret";

# Doing this to remove conflicts with protocols
export ADMIN_FRONTEND_URL=$(echo ${ADMIN_FRONTEND_URL} | sed 's|https\?://||' | sed 's|http\?://||');
export USER_FRONTEND_URL=$(echo ${USER_FRONTEND_URL} | sed 's|https\?://||' | sed 's|http\?://||');
export ADMIN_FRONTEND_URL=$(echo ${ADMIN_FRONTEND_URL} | sed 's|https\?://||' | sed 's|http\?://||');
export BACKEND_URL=$(echo ${BACKEND_URL} | sed 's|https\?://||' | sed 's|:[0-9]*||' | sed 's|http\?://||');

echo "${ADMIN_FRONTEND_URL}";

envsubst '${ADMIN_FRONTEND_URL} ${USER_FRONTEND_URL} ${BACKEND_URL} ${DEV_MODE} ${NGINX_SECRET}' < /etc/nginx/templates/nginx.conf > /etc/nginx/conf.d/default.conf;
openresty -g 'daemon off;'
