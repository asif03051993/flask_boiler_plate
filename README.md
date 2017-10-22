# Flask, SQL Alchemy, StatsD, CELERY, REDIS, FLASK MIGRATE, POSTGRES, POSTGIS

1. (Required only once, ignore this step if already done) Install postgres, start postgres.
    a. Create database 'sampledb'.
    b. Add postgis extension. run 'CREATE extension postgis;' in psql or in any postgres client.
    c. Create tables with schema in migration file.

2. Install redis (acts as cache for app and message broker for celery) and start redis. To start run
redis-server

3. To start celery worker, run
celery worker -A --concurrency=4 celery_worker.celery -l debug -Q queue1,queue2,default

4. To start application, run
python run.py

5. (Optional) To run application on test/stage/prod environment using gunicorn, run command outside sample-application directory
sample-application/venv/bin/gunicorn -c sample-application/conf/gunicorn.conf wsgi:application

6. Try hitting localhost:5000/
