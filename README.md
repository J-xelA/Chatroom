# Chatroom
Django channels chatroom

To run the SlaykCord server you will need create a virtual environment and install Django Python 3.8, and Channels:
* pip install virtualenvwrapper

In the base directory, activate your virtualenv:
* source bin/activate

Navigate to the SlaykCord folder and install requirements for your env:
* pip install -r requirements.txt

To run the server:
* docker-compose up -d
* docker-compose run --rm web python manage.py runserver

To close the server and exit your env:
* ^C
* docker-compose stop
* deactivate
