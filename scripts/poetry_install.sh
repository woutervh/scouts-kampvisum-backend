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

# https://python-poetry.org/docs/
# https://nanthony007.medium.com/stop-using-pip-use-poetry-instead-db7164f4fc72

# Using pip to install poetry avoids the need to pipe in dependencies in
# a docker.
python3.9 -m pip install poetry

# Check if it is installed correctly: poetry -version

# Run poetry init, setup basic information, and add dependencies:
# Project dependencies:
poetry add django_rest_framework
poetry add django-cors-headers
poetry add django-sql-middleware
poetry add django-storages
poetry add django-filter
poetry add mozilla_django_oidc
poetry add drf_yasg2
poetry add cffi
poetry add pyyaml
poetry add environs
poetry add future
poetry add psycopg2-binary # postgresql
poetry add ./scouts-auth-0.1.tar.gz # temporary workaround

# Let poetry download all packages and generate the poetry.lock file
poetry install

# Generate the requirements.txt
poetry export -f requirements.txt --output requirements.txt


