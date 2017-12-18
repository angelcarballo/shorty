import base64
import time
import re

from shorty.db.memory import Memory

class PersistedKey(object):
    """ Pseudo-unique keys that get persisted to a database

    This strategy generates a random key based on the current timestamp.
    The original url gets persisted to a database along with the generated key.
    Generated keys can then be used to retreive back the urls.

    If a custom key is provided, and it's valid it will be used instead of
    a randomly generated one.

    Since automatically generated keys will eventyally generate key collisions
    this strategy allows reTrying generating additional keys until a valid
    one is found.
    """

    def __init__(self, max_len=10, retries=5, db=Memory()):
        """ Constructor

        :param max_len: maximum length of keys, both custom and generated
        :param retries: number of retries for invalid generated keys
        :param db: db adapter used to persist and retrieve the keys/urls
        """
        self.max_len = max_len
        self.retries = retries
        self.db = db

    def minify(self, url, key=None):
        """ Stores the url and returns its associated key

        :param url: long url to minify
        :param key: custom key
        :return: key associated to the long url
        :raises: KeyError if a valid key could not be used/generated
        """
        if key:
            return self.__minify_with_key(url, key)
        else:
            return self.__minify_gen_key(url)

    def restore(self, key):
        """ Returns the long url associated with a given key

        :param key: key of a previously minified long url
        :return: long url
        :raises: KeyError if the key is invalid or not present
        """
        if not self.valid_key(key):
            raise KeyError(f"[{key}] is not a valid key")

        url = self.db.get_url(key)
        return url

    def valid_key(self, key):
        """ Checks if a given key's format is correct """
        pattern = re.compile("^[a-zA-Z0-9_-]{1," + str(self.max_len) + "}$")
        return pattern.match(key)

    def __minify_with_key(self, url, key):
        """ Persist the given long url and given key """
        if not self.valid_key(key):
            raise KeyError(f"[{key}] is not a valid key")
        self.db.store_url(key, url)
        return key

    def __minify_gen_key(self, url):
        """ Persist the given long url a generated key """
        for time in range(0, self.retries):
            try:
                key = self.__generate_key(url)
                self.db.store_url(key, url)
                return key
            except KeyError:
                continue
            break
        raise KeyError(f"key generation failed after {self.retries} attempts")


    def __generate_key(self, url):
        """ Generates a pseudo-random key for a given long url

        Key generation steps:
         - get miliseconds since Epoch
         - transform to bytes
         - encode bytes on base64 (avoiding non-url safe characters)
         - remove padding
         - enforce max key length truncating the key
        """
        int_key = int(time.time() * 1000)
        bytes_length = (int_key.bit_length() + 7) // 8
        bytes_key = int_key.to_bytes(bytes_length, byteorder="big")
        key_with_padding = base64.urlsafe_b64encode(bytes_key).decode()
        key = key_with_padding.replace("=", "")
        return key[0:self.max_len - 1:]

