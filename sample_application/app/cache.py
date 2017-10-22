from flask_cache import Cache as FlaskCache

class Cache(FlaskCache):
    """
        Defining some functions which flask cache doesn't provide.
    """
    def __init__(self):
        FlaskCache.__init__(self)

    def inc(self, *args, **kwargs):
        """
            Proxy function for internal cache object.
            initial_value = sets initial value if key doesn't exist
        """
        initial_value = kwargs.get('initial_value', None)
        kwargs.pop('initial_value')
        if not self.get(*args):
            if initial_value:
                set_kwargs = dict(value=initial_value)
                self.set(*args, **set_kwargs)
            else:
                return None
        return self.cache.inc(*args, **kwargs)

    def dec(self, *args, **kwargs):
        """
            Proxy function for internal cache object.
            initial_value = sets initial value if key doesn't exist
        """
        initial_value = kwargs.get('initial_value', None)
        kwargs.pop('initial_value')
        if not self.get(*args):
            if initial_value:
                set_kwargs = dict(value=initial_value)
                self.set(*args, **set_kwargs)
            else:
                return None
        return self.cache.dec(*args, **kwargs)

    def set_multi(self, *args, **kwargs):
        return self.cache.set_many(*args, **kwargs)

cache = Cache()