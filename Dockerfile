FROM python:3.6

MAINTAINER Allan Maina

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /src

WORKDIR /src

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

CMD exec gunicorn edms.wsgi:application - bind  0.0.0.0:8000 - workers 40

EXPOSE 8000
