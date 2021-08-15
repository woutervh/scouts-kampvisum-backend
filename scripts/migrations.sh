#!/bin/bash

APPS=("base" "groupadmin" "scouts_camp_visums" "scouts_groups" "scouts_camps")
FIXTURES=("scouts_group_types.json" "scouts_section_names.json" "scouts_camp_visum_categories.json" "scouts_camp_visum_sub_categories.json")

make_migration() {
	echo "============================================================"
	echo "MAKING MIGRATIONS FOR $1"
	echo "============================================================"
	python manage.py makemigrations $1
}

load_fixture() {
	echo "============================================================"
	echo "LOADING DATA: $1"
	echo "============================================================"
	python manage.py loaddata $1
}

for APP in ${APPS[@]}; do
	make_migration $APP
done

echo "============================================================"
echo "RUNNING makemigrations"
echo "============================================================"
python manage.py makemigrations

echo "============================================================"
echo "RUNNING migrate"
echo "============================================================"
python manage.py migrate --run-syncdb

for FIXTURE in ${FIXTURES[@]}; do
	load_fixture $FIXTURE
done
