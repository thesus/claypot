# Build JavaScript code
FROM node:alpine as js
COPY frontend/ /code/
RUN cd /code \
    && npm install -g yarn \
    && yarn install \
    && yarn build --mode production

# Setup Caddy
FROM abiosoft/caddy
ENV ACME_AGREE=true
COPY compose/caddy/Caddyfile /etc/Caddyfile
COPY --from=js /code/dist/ /var/www/html
