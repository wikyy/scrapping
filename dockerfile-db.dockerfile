FROM alpine

RUN apk add --no-cache sqlite

VOLUME /data

CMD ["sqlite3", "/data/db.sqlite3"]
