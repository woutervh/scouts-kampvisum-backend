#!/bin/bash

python manage.py makemigrations scouts_auth
python manage.py makemigrations base
python manage.py makemigrations scouts_camp_visums
python manage.py makemigrations scouts_camps
python manage.py makemigrations scouts_groups
python manage.py makemigrations
python manage.py migrate

python manage.py loaddata scouts_group_types.json
python manage.py loaddata scouts_section_names.json
python manage.py loaddata scouts_camp_visum_categories.json
python manage.py loaddata scouts_camp_visum_sub_categories.json

