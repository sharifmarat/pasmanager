FROM alpine:3.14.0

EXPOSE 80

ENV KEY_DB=/var/db/keys.sqlite

RUN apk update && \
    apk add --no-cache \
    lighttpd \
    python3 \
    py3-pip \
    sqlite \
    curl \
    && pip3 install pyotp \
    && pip3 install Flask \
    && rm -rf /var/cache/apk/* \
    && mkdir -p /var/db \
    && chown lighttpd:lighttpd /var/db

ADD html /var/www/localhost/
COPY src/* /etc/lighttpd/

HEALTHCHECK --interval=10m --timeout=1s \
  CMD curl -f http://localhost/ || exit 1

ENTRYPOINT ["/usr/sbin/lighttpd", "-D", "-f", "/etc/lighttpd/lighttpd.conf"]
