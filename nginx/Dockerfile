FROM openresty/openresty:alpine

RUN apk add --no-cache imagemagick
RUN apk add --no-cache gettext

COPY ./certs/* /etc/nginx/certs/
COPY nginx.conf /etc/nginx/templates/
COPY entrypoint.sh .
COPY app.lua /lua/
ENTRYPOINT [ "/entrypoint.sh" ]
