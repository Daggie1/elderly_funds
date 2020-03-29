FROM python:3.6

MAINTAINER Allan

ENV PYTHONUNBUFFERED 1

RUN mkdir /edms

WORKDIR /edms

ADD requirements.txt /edms/

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

RUN pip install -r requirements.txt


ADD . /edms/

EXPOSE 8000