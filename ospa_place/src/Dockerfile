FROM python:3.12-slim

WORKDIR /app

COPY src /app/

USER root

RUN pip install -r requirements.txt

CMD [ "tail", "-f", "/dev/null" ]
