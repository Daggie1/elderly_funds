##EDMS 
### ministry for interior
This is an Electronic Document Management System made in django.

#### Deployment

It uses Docker, 
To Build Run:
`docker-compose up -d --build`

###Configurations
Get into the docker container `docker exec -it edms_web_1 bash`

Then execute the following necessary commands

`python3 manage.py makemigrations`

`python3 manage.py migrate`

`python3 manage.py collectstatic`

`python3 manage.py loaddata fixtures.json`

`python3 manage.py loaddata states.json`

_Please dont automate this with a bash script_

Remember to create a superuser