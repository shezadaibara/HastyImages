#!/bin/sh

# Start Gunicorn processes
echo Running Migration.
python manage.py migrate


echo Starting Gunicorn.
gunicorn application.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2