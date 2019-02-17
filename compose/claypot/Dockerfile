FROM python
COPY requirements/ /tmp/requirements
RUN pip install -r /tmp/requirements/production.txt \
    && rm -rf /tmp/requirements
COPY config/ /code/config
COPY claypot/ /code/claypot
WORKDIR "/code"

CMD ["gunicorn", "-b", "0.0.0.0:80", "-w", "1", "config.wsgi"]
