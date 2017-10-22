import os
from flask import Flask, render_template

import pkgutil
import importlib

from monitoring.client import StatsD
from raven.contrib.flask import Sentry
from database import db
from cache import cache
from celery import Celery
import server_config

# setting default time zone of app to utc.
os.environ['TZ'] = 'UTC'

# set up
statsd = StatsD()
sentry = None
if server_config['TYPE'] != 'LOCAL':
    sentry = Sentry()

celery = Celery(__name__, broker=server_config.CELERY_BROKER_URL)

def configure_celery(app):
    package_prefix = __name__ + '.'
    module_names = []
    for importer, module_name, ispkg in pkgutil.iter_modules([os.path.dirname(__file__)]):
        module_names.append(package_prefix + module_name)

    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    celery.autodiscover_tasks(module_names, force=True)


def configure_urls(app):
    # add url rules (i.e, routes)
    from user.urls import urls
    for url in urls:
        app.add_url_rule(url[0], methods=url[1], view_func=url[2])

def create_app(config_name):
    if config_name is None:
        config_name = 'server_config'

    # app set up
    app = Flask(__name__)
    app.config.from_object(config_name)
    statsd.init_app(app)
    if sentry:
        # sentry dsn mentioned below is dummy.
        sentry.init_app(
            app, dsn='https://dummy1:dummy2@sentry.io/12345')
        # Adding tags to distinguish dev, test and prod environment errors in sentry.
        sentry.tags_context({
            'environment': server_config['TYPE'],
        })

    with app.app_context():
        db.init_app(app)
        cache.init_app(app)
        configure_celery(app)

        # Import a module / component using its blueprint handler variable
        from user.views import user_module

        # Register blueprints
        app.register_blueprint(user_module)

        # set up urls
        configure_urls(app)

        @app.route('/', methods=['GET'])
        def index():
             return ("Welcome! Sample Application is active!", 200, {"Content-Type" : 'text/plain'})

        @app.route('/<path:path>')
        def static_file(path):
             return app.send_static_file(path)


    return app

