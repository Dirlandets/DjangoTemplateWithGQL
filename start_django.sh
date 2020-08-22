#!/bin/bash
set -e


if [ "$ENV" = 'PROD' ]; then
    echo "PRODUCTION" 
    exec gunicorn --bind 0.0.0.0:8000 --user app --workers 4 app.wsgi:application --log-file -
elif [ "$ENV" = 'MIGRATE' ]; then
    echo "MIGRATE" 
    exec python manage.py migrate --noinput
else
    echo "DEVELOP"
    # python manage.py collectstatic --noinput
    exec python manage.py runserver 0.0.0.0:8000
fi
