#!/bin/bash

until dockerize -wait tcp://db:3306 -timeout 60s
do
    echo "Waiting for database to be ready..."
    sleep 5
done

echo "Database is ready. Applying migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Starting the Django development server..."
exec "$@"