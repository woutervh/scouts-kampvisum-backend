#!/bin/bash

python manage.py makemigrations scouts_auth
python manage.py makemigrations base
python manage.py makemigrations scouts_camps
python manage.py makemigrations scouts_groups
python manage.py makemigrations
python manage.py migrate

python manage.py loaddata scouts_troop_names.json