FROM python:3.8-slim

WORKDIR /opt/app

RUN python3 -m pip install pipenv

ENV PIPENV_VENV_IN_PROJECT=1

ADD ./Pipfile.lock /opt/app

RUN pipenv sync 

ADD . /opt/app

ARG TG_API_KEY

CMD [".venv/bin/python", "application.py"]
