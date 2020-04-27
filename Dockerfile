FROM python:3.6


ENV PYTHONUNBUFFERED 1

RUN mkdir /edms
WORKDIR /edms
COPY . /edms


RUN pip install  -r requirements.txt







#
#ENV PYTHONUNBUFFERED 1
#
#RUN mkdir /edms
#
#WORKDIR /edms
#
#COPY requirements.txt ./
#
#
#
#COPY . .
#
#CMD exec gunicorn edms.wsgi:application - bind  0.0.0.0:8000 - workers 3

