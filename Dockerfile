#enclopedia backend docker image
FROM python:3.8-slim-buster
ENV APP_HOME=/subscription_app
WORKDIR /subscription-app
LABEL maintainer="info@enclopediai-info.com"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
COPY ./requirements.txt /requirements.txt
COPY ./ /subscription-app

RUN apt-get update \
   && apt-get install -y build-essential \
   && apt-get install -u -y postgresql-client libjpeg-dev libpq-dev libffi-dev musl-dev \
   && apt-get install -u -y --no-install-recommends libc-dev postgresql \
   && apt-get install -u -y --no-install-recommends  netcat \
   && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
   && apt-get clean \
   && rm -rf /var/lib/apt/lists/* \
   && mkdir $APP_HOME \
   && mkdir $APP_HOME/static \
   && mkdir $APP_HOME/media \
   && pip3 install --upgrade pip  \
   && pip install -r /requirements.txt 

EXPOSE 8000