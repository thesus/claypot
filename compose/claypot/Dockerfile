FROM node:10-alpine as js
COPY frontend/ /code/frontend/

RUN cd /code/frontend/ \
    && yarn install \
    && yarn build --mode production

FROM python:3.8 as base
COPY requirements/ /tmp/requirements
RUN pip install -r /tmp/requirements/production.txt \
    && rm -rf /tmp/requirements
COPY --from=js /code/claypot/templates/claypot/index.html /code/claypot/templates/claypot/index.html
COPY manage.py /code/manage.py
COPY config/ /code/config
COPY claypot/ /code/claypot
WORKDIR "/code"

# We take a detour to compile message objects, but keep the
# additional footprint of gettext out of the final image.
FROM base as compile-messages
RUN apt-get update \
    && apt-get install -y gettext \
    # These environment variables are required to pacify manage.py.
    # It will not run our command otherwise.
    && DATABASE_URL=sqlite://:memory: DJANGO_SECRET_KEY=set ./manage.py compilemessages \
    && find . -name '*.mo' | xargs tar -cf /code/all-translations.tar

FROM base
COPY --from=compile-messages /code/all-translations.tar /code/all-translations.tar
RUN tar -xf all-translations.tar \
    && rm all-translations.tar
CMD ["gunicorn", "-b", "0.0.0.0:80", "-w", "1", "config.wsgi"]
