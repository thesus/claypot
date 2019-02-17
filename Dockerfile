FROM node:alpine as js
COPY frontend/ /code/
RUN cd /code \
    && npm install -g yarn \
    && yarn install \
    && yarn build --mode production

FROM python
COPY requirements/ /tmp/requirements
RUN pip install -r /tmp/requirements/production.txt \
    && rm -rf /tmp/requirements
COPY config/ /code/config
COPY claypot/ /code/claypot
COPY --from=js /code/dist/ /code/contrib
