#! /bin/bash

python /app/bin/database_check.py
while [[ $? != 0 ]] ; do
    sleep 5; echo "*** Waiting for postgres container ..."
    python /app/bin/database_check.py
done

echo "==> Django setup, executing: migrate"
python /app/django/manage.py makemigrations
python /app/django/manage.py migrate
#echo "==> Django setup, executing: makemessages"
#python /usr/src/app/${DJANGO_PROJECT_NAME}/manage.py makemessages
echo "==> Django setup, executing: collectstatic"
python /app/django/manage.py collectstatic --noinput -v 3

#/app/bin/dummy.sh


cd django
gunicorn app.wsgi:application -c ../bin/gunicorn.conf.py
