FROM postgres:alpine3.18

RUN apk add --no-cache nano

COPY tables_construction.sql /docker-entrypoint-initdb.d/
