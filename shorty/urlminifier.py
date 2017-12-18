import re

from shorty.strategy.persisted_key import PersistedKey

class UrlMinifier(object):
    """ Generates short versions of URLs

    Short URLs can be generated using different strategies.
    Check the documentation for each strategy to understand their
    differences and limitations.
    """

    def __init__(self, domain, strategy=PersistedKey()):
        """ Constructor

        :param domain: Domain including protocol to be used on generated urls.
        :param strategy: Used to minify and restore urls.
        """
        self.domain = domain
        self.strategy = strategy

    def minify(self, original_url, requested_key=None):
        """ Generates a short url for a given long url

        :param original_url: Url to shorten
        :param requested_key: Desired short url (only key)
        :return: Generated short url
        :raises: ValueError if the requested key is not valid
        """
        short_url = self.strategy.minify(original_url, requested_key)
        return f"{self.domain}/{short_url}"

    def restore(self, shortened_url):
        """ Fetches the long version of a previously shortened url

        :param shortened_url: Previously shortened url
        :return: Original long url
        :raises: ValueError if the original url cannot be restored
        """
        key = self.__extract_key(shortened_url)
        return self.strategy.restore(key)

    def __extract_key(self, shortened_url):
        """ Removes protocol and domain from a shortened url

        :param shortened_url: Previously shortened url
        :return: Unique part (key) of the shortened url
        :raises: ValueError if the key cannot be extracted
        """
        pattern = re.compile("^%s/(?P<key>.*)$" % self.domain)
        match = pattern.match(shortened_url)
        if not match:
            raise ValueError(f"{shortened_url} is not a valid short url")
        return match.group("key")

