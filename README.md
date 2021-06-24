Image contains a docker image with a trivial pass manager (sqlite3 + python + html + lighttpd).

# Building

```
docker build --rm -t pmanager .
```

# Initializing DB

TODO

# Running

```
docker run \
    --name pmanager \
    --restart=on-failure \
    -e KEY_DB="/var/db/keys.sqlite" \
    -p 127.0.0.1:8888:80 \
    -d \
    -v <PATH_TO_DB>:/var/db/keys.sqlite \
    pmanager
```

## Reverse proxy from nginx
```
location /<location>/ {
        proxy_pass       http://127.0.0.1:8888/;
        proxy_set_header Host            $host;
        proxy_set_header X-Forwarded-For $remote_addr;
        auth_basic            "extra protection";
        auth_basic_user_file  <auth-file>; 
```
