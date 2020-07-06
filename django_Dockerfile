FROM python:3.6

MAINTAINER douglas57

ENV PYTHONUNBUFFERED 1

COPY . /src

WORKDIR /src

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

CMD python manage.py runserver 0.0.0.0:8000
#CMD exec gunicorn edms.wsgi:application - bind  0.0.0.0:8000 - workers 40

EXPOSE 8000
