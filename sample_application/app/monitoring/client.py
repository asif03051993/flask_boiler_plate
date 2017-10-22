import time

from statsd import StatsClient
from flask import g, request

class StatsD(object):
    def __init__(self, app=None, config=None):
        self.config = None
        self.statsd = None

        if app is not None:
            self.init_app(app, config=config)
        else:
            self.app = None

    def init_app(self, app, config=None):
        if config is not None:
            self.config = config
        elif self.config is None:
            self.config = app.config

        self.config.setdefault('STATSD_HOST', 'localhost')
        self.config.setdefault('STATSD_PORT', 8125)
        self.config.setdefault('STATSD_PREFIX', None)

        self.app = app

        self.statsd = StatsClient(self.config['STATSD_HOST'],
            self.config['STATSD_PORT'], self.config['STATSD_PREFIX'])

        self.use_ms=self.config.get('STATSD_USEMS', True)

        # Configure any of our middleware
        self.setup_middleware()

    def timer(self, *args, **kwargs):
        return self.statsd.timer(*args, **kwargs)

    def timing(self, *args, **kwargs):
        return self.statsd.timing(*args, **kwargs)

    def incr(self, *args, **kwargs):
        return self.statsd.incr(*args, **kwargs)

    def decr(self, *args, **kwargs):
        return self.statsd.decr(*args, **kwargs)

    def gauge(self, *args, **kwargs):
        return self.statsd.gauge(*args, **kwargs)

    def setup_middleware(self):
        """Helper to configure/setup any Flask-StatsD middleware"""
        # Configure response time middleware (if desired)
        self.config.setdefault('STATSD_CONFIGURE_MIDDLEWARE', True)
        self.config.setdefault('STATSD_RESPONSE_METRIC_NAME', 'response.time')
        self.config.setdefault('STATSD_NUMBER_OF_REQUESTS_METRIC_NAME', 'request.api')
        self.config.setdefault('STATSD_RESPONSE_SAMPLE_RATE', 1)
        self.config.setdefault('STATSD_RESPONSE_AUTO_TAG', True)
        self.config.setdefault('STATSD_RESPONSE_ENDPOINT_TAG_FORMAT', 'endpoint_{0}')
        self.config.setdefault('STATSD_RESPONSE_METHOD_TAG_FORMAT', 'method_{0}')
        if self.config['STATSD_CONFIGURE_MIDDLEWARE']:
            self.app.before_request(self.before_request)
            self.app.after_request(self.after_request)

    def before_request(self):
        """
        statsd middleware handle for before each request
        """
        # Set the request start time
        g.flask_statsd_start_time = time.time()
        g.flask_statsd_request_tags = []

        # Add some default request tags
        if self.config['STATSD_RESPONSE_AUTO_TAG']:
            self.add_request_tags([
                # Endpoint tag
                self.config['STATSD_RESPONSE_ENDPOINT_TAG_FORMAT'].format(str(request.endpoint).lower()),
                # Method tag
                self.config['STATSD_RESPONSE_METHOD_TAG_FORMAT'].format(request.method.lower()),
            ])

        # Send no of requests per second
        metric = '.'.join([self.config['STATSD_NUMBER_OF_REQUESTS_METRIC_NAME'],
                           str(request.endpoint).lower(), request.method.lower()])
        self.statsd.incr(metric, 1)


    def after_request(self, response):
        """
         statsd middleware handler for after each request

        :param response: the response to be sent to the client
        :type response: ``flask.Response``
        :rtype: ``flask.Response``
        """
        # Return early if we don't have the start time
        if not hasattr(g, 'flask_statsd_start_time'):
            return response

        # Get the response time for this request
        elapsed = time.time() - g.flask_statsd_start_time
        # Convert the elapsed time to milliseconds if they want them
        if self.use_ms:
            elapsed = int(round(1000 * elapsed))

        # Add some additional response tags
        if self.config['STATSD_RESPONSE_AUTO_TAG']:
            self.add_request_tags(['status_code_%s' % (response.status_code, )])

        metric = self.config['STATSD_RESPONSE_METRIC_NAME']
        tags = self.get_request_tags()
        if tags:
            metric = ".".join([metric] + tags)

        # Emit our timing metric
        self.statsd.timing(metric,
                           elapsed, rate=self.config['STATSD_RESPONSE_SAMPLE_RATE'])

        # We ALWAYS have to return the original response
        return response
    
    def get_request_tags(self):
        """
        Get the current list of tags set for this request

        :rtype: list
        """
        return getattr(g, 'flask_statsd_request_tags', [])

    def add_request_tags(self, tags):
        """
        Add the provided list of tags to the tags stored for this request

        :param tags: tags to add to this requests tags
        :type tags: list
        :rtype: list
        """
        # Get the current list of tags to append to
        # DEV: We use this method since ``self.get_request_tags`` will ensure that we get a list back
        current_tags = self.get_request_tags()

        # Append our new tags, and return the new full list of tags for this request
        g.flask_statsd_request_tags = current_tags + tags
        return g.flask_statsd_request_tags

