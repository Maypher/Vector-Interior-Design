FROM openresty/openresty:alpine

RUN apk add --no-cache imagemagick
RUN apk add --no-cache gettext

COPY nginx.conf /etc/nginx/templates/
COPY includes /usr/local/openresty/nginx/conf/includes/
COPY errors /usr/local/openresty/nginx/conf/errors/
COPY entrypoint.sh .
COPY app.lua /lua/

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
