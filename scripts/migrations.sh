#!/bin/bash

echo "============================================================"
echo "MAKING MIGRATIONS FOR base
echo "============================================================"
python manage.py makemigrations base
echo "============================================================"
echo "MAKING MIGRATIONS FOR scouts_camp_visums
echo "============================================================"
python manage.py makemigrations scouts_camp_visums
echo "============================================================"
echo "MAKING MIGRATIONS FOR scouts_camps
echo "============================================================"
python manage.py makemigrations scouts_camps
echo "============================================================"
echo "MAKING MIGRATIONS FOR scouts_groups
echo "============================================================"
python manage.py makemigrations scouts_groups

python manage.py makemigrations
python manage.py migrate

python manage.py loaddata scouts_group_types.json
python manage.py loaddata scouts_section_names.json
python manage.py loaddata scouts_camp_visum_categories.json
python manage.py loaddata scouts_camp_visum_sub_categories.json

