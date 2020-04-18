FROM python:3.6

RUN mkdir /edms
WORKDIR /edms

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


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