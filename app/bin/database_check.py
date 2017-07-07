#!/usr/bin/env python
import os
import sys
import psycopg2


# NOTE: check if this works
def database_check():
    dbname = os.environ.get('POSTGRES_DB')
    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')
    host = os.environ.get('POSTGRES_HOST')
    port = os.environ.get('POSTGRES_PORT')

    try:
        psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    except:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    database_check()
