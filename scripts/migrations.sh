#!/bin/bash

# DON'T PUT ANY CODE BEFORE THESE VARIABLES, OTHERWISE THE VARIABLE IMPORT
# IN OTHER SCRIPTS WON'T WORK
APPS=(
	"admin"
	"auth"
	"scouts_auth"
	"participants"
	"locations"
	"groups"
	"camps"
	"visums"
)
FIXTURES=(
	"scouts_group_types.json"
	"scouts_section_names.json"
	"default_scouts_section_names.json"
	"camp_types.json"
	"category_set_priorities.json"
	"check_types.json"
)
# RETURN IF CALLED TO IMPORT VARIABLES
[[ "${#BASH_SOURCE[@]}" -gt "1" ]] && { return 0; }
# SAFE TO ADD CODE BELOW

# Generated at http://patorjk.com/software/taag/
cat << "EOF"
##############################################################################
##############################################################################
###                                                                        ###
###                                                                        ###
###                       _             _ _                                ###
###                      (_)_ __  _   _(_) |_ ___                          ###
###                      | | '_ \| | | | | __/ __|                         ###
###                      | | | | | |_| | | |_\__ \                         ###
###                      |_|_| |_|\__,_|_|\__|___/                         ###
###                                                                        ###
###                                                                        ###
##############################################################################
##############################################################################
EOF

DJANGO_MANAGE_DIR="scouts_kampvisum_api"
# Assume that the script is called from the root of the application directory 
SCRIPT_DIR=$PWD
# Check to see if it is called by a script in the root directory
if [[ $2 ]]; then
	SCRIPT_DIR=$(ps -o args= $PPID)
	set -- $SCRIPT_DIR
	SCRIPT_DIR=$(dirname $2)
	SCRIPT_DIR=$(realpath $SCRIPT_DIR)
fi

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
	python manage.py loaddata --natural $1
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
