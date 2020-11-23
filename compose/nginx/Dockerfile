# Build JavaScript code
FROM node:10-alpine as js
COPY frontend/ /code/frontend/

RUN cd /code/frontend \
    && yarn install \
    && yarn build --mode production

# Build nginx container
FROM nginx:alpine
COPY compose/nginx/default.conf /etc/nginx/conf.d/default.conf

COPY --from=js /code/claypot/templates/claypot/js/ /var/www/html/js/
COPY --from=js /code/claypot/templates/claypot/css/ /var/www/html/css/
