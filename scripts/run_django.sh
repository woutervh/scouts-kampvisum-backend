#!/bin/bash

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

# Assume that the script is called from the root of the application directory 
SCRIPT_DIR=$PWD
DJANGO_MANAGE_DIR="scouts_kampvisum_api"
# Check to see if it is called by a script in the root directory
if [[ $2 ]]; then
	SCRIPT_DIR=$(ps -o args= $PPID)
	set -- $SCRIPT_DIR
	SCRIPT_DIR=$(dirname $2)
	SCRIPT_DIR=$(realpath $SCRIPT_DIR)

    cd "$SCRIPT_DIR/$DJANGO_MANAGE_DIR"
fi

# https://docs.djangoproject.com/en/dev/ref/django-admin/#syntax-coloring
export DJANGO_COLORS="dark;error=red,bold"
echo "$SCRIPT_DIR"
export PYTHONPATH="$SCRIPT_DIR"
python manage.py runserver
