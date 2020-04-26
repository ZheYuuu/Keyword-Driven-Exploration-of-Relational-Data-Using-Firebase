FROM python:3.6-slim-buster

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential python3-dev vim
RUN pip install -r requirements.txt && pip install gunicorn

CMD gunicorn apps:app -c ./gunicorn.cfg.py