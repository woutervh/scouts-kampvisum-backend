#!/bin/bash

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

# Clean __pycache__
py3clean .

# Remove previous migrations (only do this in dev !)
rm -rf $(find . -type d -name "migrations")

# Remove existing sqlite databases
rm -rf $(find . -type f -name "*.sqlite3")