# Build JavaScript code
FROM node:10-alpine as js
COPY frontend/ /code/

RUN cd /code \
    && yarn install \
    && yarn build --mode production

# Build nginx container
FROM nginx:alpine
COPY compose/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=js /code/dist/ /var/www/html
