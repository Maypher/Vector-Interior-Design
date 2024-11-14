FROM postgres:latest

RUN apt-get update && apt-get install -y locales \
    && localedef -i es_ES -c -f UTF-8 -A /usr/share/locale/locale.alias es_ES.UTF-8

# Set locale environment variables
ENV LANG es_ES.UTF-8
ENV LANGUAGE es_ES:es
ENV LC_ALL es_ES.UTF-8

COPY . ./docker-entrypoint-initdb.d
