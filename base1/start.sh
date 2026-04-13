#!/bin/bash
# Run migrations before starting the server
python manage.py migrate --noinput
# Start the application using Gunicorn
gunicorn base1.wsgi --bind 0.0.0.0:$PORT
