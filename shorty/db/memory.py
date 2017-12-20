import time

class Memory(object):
    """ Db adapter that stores urls and users in memory

    This db adapter is mostly used for tests.
    """

    def __init__(self):
        self.urls = {}
        self.users = {}

    def store_url(self, key, url):
        """ Stores the given key/url on memory. Raises if key present """
        if self.has_key(key):
            raise KeyError(f"key [{key}] is already in use")
        self.urls[key] = { 'url': url, 'created_at': time.time() }

    def get_url(self, key):
        """ Returns the url associated with the key. Raises if key missing """
        if not self.has_key(key):
            raise KeyError(f"Unknown key [{key}]")
        return self.urls[key]['url']

    def has_key(self, key):
        """ Checks if the key is present on the url db """
        return key in self.urls

    def store_user(self, user):
        """ Stores the given user on memory. Raises if email present """
        if self.has_user(user.email):
            raise KeyError(f"User [{user.email}] already exists")
        self.users[user.email] = user

    def get_user(self, email):
        """ Returns the user associated with the email. Raises if not present """
        if not self.has_user(email):
            raise KeyError(f"Unknown user [{email}]")
        return self.users[email]

    def has_user(self, email):
        """ Checks if the email is present on the user db """
        return email in self.users


