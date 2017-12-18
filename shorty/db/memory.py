import time

class Memory(object):
    """ Db adapter that stores urls in memory

    This db adapter is mostly used for tests.
    """

    def __init__(self):
        self.entries = {}

    def store_url(self, key, url):
        """ Stores the given key/url on memory. Raises if key present """
        if self.has_key(key):
            raise KeyError(f"key [{key}] is already in use")
        self.entries[key] = { 'url': url, 'created_at': time.time() }

    def get_url(self, key):
        """ Returns the url associated with the key. Raises if key missing """
        if not self.has_key(key):
            raise KeyError(f"Unknown key [{key}]")
        return self.entries[key]['url']

    def has_key(self, key):
        """ Checks if the key is present on the db """
        return key in self.entries

