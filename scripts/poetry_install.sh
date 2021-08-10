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

# !!!
# Don't use this script when building dependencies for a docker
# Users can't be expected to have the necessary software installed to make
# the builds.
# For dockers: build everything inside the docker.
# Use this script when testing the app locally (development env).
# !!!

# DOCUMENTATION USED:
# https://python-poetry.org/docs/
# https://nanthony007.medium.com/stop-using-pip-use-poetry-instead-db7164f4fc72

# Using pip to install poetry avoids the need to pipe in dependencies in
# a docker when installing poetry there.
python -m pip install poetry

# To check if it is installed correctly: poetry -version

# Remove any existing version of this package
echo "Removing existing scouts-auth with poetry"
poetry remove scouts-auth

# Run poetry init and setup basic information
poetry init

# Setup repo for scouts-auth
poetry config repositories.scouts-auth https://gitlab.inuits.io/boro/
poetry config certificates.scouts-auth.client-cert ./inuits_docker.pub

# Add project dependencies:
poetry add django_rest_framework
poetry add django-cors-headers
poetry add django-sql-middleware
poetry add django-storages
poetry add django-filter
poetry add django-safedelete
poetry add drf_yasg2
poetry add cffi
poetry add pyyaml
poetry add environs
poetry add future
poetry add psycopg2-binary # postgresql
poetry add git+ssh://git@gitlab.inuits.io:2224/boro/scouts_auth.git#master

# Let poetry download all packages and generate the poetry.lock file
poetry install

# Generate the requirements.txt
poetry export -f requirements.txt --output requirements.txt

