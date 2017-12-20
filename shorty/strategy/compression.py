class Compression(object):
    """ Key generation basd on small string compression

    This strategy generates a key compressing the long url.
    The original long url can then be recovered decompressing the generated
    key.

    Custom keys are not supported.

    Keeping max key length will not always be possible, depending on the size
    of the original url.
    """
    def __init__(self, max_len=10):
        """ Constructor

        :param max_len: maximum length of keys
        """
        self.max_len = max_len

    def minify(self, url, key=None):
        """ Stores the url and returns its associated key

        :param url: long url to minify
        :param key: custom key (not supported)
        :return: key associated to the long url
        """
        if key:
            raise NotImplementedError("Compression: custom keys not supported")
        else:
            key = self.__compress(url)
            return key

    def restore(self, key):
        """ Returns the long url associated with a given key

        :param key: key of a previously minified long url
        :return: long url
        """
        url = self.__uncompress(key)
        return url

    def self.__compress(url):
        raise NotImplementedError()

    def self.__uncompress(key):
        raise NotImplementedError()
