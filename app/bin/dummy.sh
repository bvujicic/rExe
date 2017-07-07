#!/usr/bin/env bash

python manage.py dummydata_users
python manage.py dummydata_articles
python manage.py createsuperuser --username=admin
