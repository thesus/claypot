# Build JavaScript code
FROM node:10-alpine as js
COPY frontend/ /code/
RUN cd /code \
    && npm install -g yarn \
    && yarn install \
    && yarn build --mode production

# Borrowed from https://github.com/abiosoft/caddy-docker/blob/master/Dockerfile-no-stats
# -- snip --
#
# Builder
#
FROM abiosoft/caddy:builder as builder

ARG version="1.0.0"
ARG plugins="git,cors,realip,expires,cache"

# process wrapper
RUN go get -v github.com/abiosoft/parent

RUN VERSION=${version} PLUGINS=${plugins} ENABLE_TELEMETRY=false /bin/sh /usr/bin/builder.sh

#
# Final stage
#
FROM alpine:3.8
LABEL maintainer "Abiola Ibrahim <abiola89@gmail.com>"

ARG version="1.0.0"
LABEL caddy_version="$version"

# Let's Encrypt Agreement
ENV ACME_AGREE="false"

# Telemetry Stats
ENV ENABLE_TELEMETRY="false"

RUN apk add --no-cache openssh-client git

# install caddy
COPY --from=builder /install/caddy /usr/bin/caddy

# validate install
RUN /usr/bin/caddy -version
RUN /usr/bin/caddy -plugins

EXPOSE 80 443 2015
VOLUME /root/.caddy /srv
WORKDIR /srv

# install process wrapper
COPY --from=builder /go/bin/parent /bin/parent

ENTRYPOINT ["/bin/parent", "caddy"]
CMD ["--conf", "/etc/Caddyfile", "--log", "stdout", "--agree=$ACME_AGREE"]

# -- snip --

ENV ACME_AGREE=true
COPY compose/caddy/Caddyfile /etc/Caddyfile
COPY --from=js /code/dist/ /var/www/html
