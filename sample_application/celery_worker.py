#!/usr/bin/env python
"""
    To start celery worker, run command
    celery worker -A --concurrency=4 celery_worker.celery -l debug -Q queue1,queue2,default
"""

from app import celery, create_app

app = create_app(config_name = 'server_config')
app.app_context().push()

