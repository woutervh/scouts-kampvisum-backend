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
# Check to see if it is called by a script in the root directory
if [[ $2 ]]; then
	SCRIPT_DIR=$(ps -o args= $PPID)
	set -- $SCRIPT_DIR
	SCRIPT_DIR=$(dirname $2)
	SCRIPT_DIR=$(realpath $SCRIPT_DIR)
fi

if [[ -d "$SCRIPT_DIR/lib" ]]; then
	if [[ -d "$SCRIPT_DIR/lib/scouts-auth" ]]; then
		sudo rm -rf "$SCRIPT_DIR/lib/scouts-auth"
	fi
else
	mkdir -p "$SCRIPT_DIR/lib"
fi

cd "$SCRIPT_DIR/lib"
git clone ssh://git@gitlab.inuits.io:2224/boro/scouts_auth.git scouts-auth

cd "$SCRIPT_DIR/lib/scouts-auth"
poetry build

if [[ $? -eq 0 ]]; then
	cp -pR "./dist/"* "$SCRIPT_DIR/lib"
	sudo rm -rf "$SCRIPT_DIR/lib/scouts-auth"
fi

cd "$SCRIPT_DIR"


# Install the lib with pip, to run without poetry
python -m pip uninstall scouts_auth
python -m pip install lib/scouts_auth-0.1.0.tar.gz