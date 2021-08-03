#!/bin/sh

set -e

if [ "$1" = "--do-migrate" ]; then
  echo "Running migrations..."
  if ! ./manage.py migrate; then
    exit 1
  fi
else
  echo "Skipping migration..."
fi

echo "Starting development server..."
exec ./manage.py runserver 0.0.0.0:8000
