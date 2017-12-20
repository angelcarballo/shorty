import re

from shorty.strategy.persisted_key import PersistedKey
from shorty.data.event_handler import EventHandler
from shorty.data.events import UrlMinified, UrlRestored

class UrlMinifier(object):
    """ Generates short versions of URLs

    Short URLs can be generated using different strategies.
    Check the documentation for each strategy to understand their
    differences and limitations.
    """

    def __init__(
        self, domain, strategy=PersistedKey(), event_handler=EventHandler()):
        """ Constructor

        :param domain: Domain including protocol to be used on generated urls.
        :param strategy: Used to minify and restore urls.
        :param event_handler: used to send events
        """
        self.domain = domain
        self.strategy = strategy
        self.event_handler = event_handler

    def minify(self, long_url, user_id, requested_key=None):
        """ Generates a short url for a given long url

        :param long_url: Url to shorten
        :param requested_key: Desired short url (only key)
        :return: Generated short url
        :raises: ValueError if the requested key is not valid
        """
        key = self.strategy.minify(long_url, requested_key)
        short_url = f"{self.domain}/{key}"

        event = UrlMinified(long_url, short_url, user_id)
        self.event_handler.send_event(event)

        return short_url

    def restore(self, short_url):
        """ Fetches the long version of a previously shortened url

        :param shortened_url: Previously shortened url
        :return: Original long url
        :raises: ValueError if the original url cannot be restored
        """
        key = self.__extract_key(short_url)
        long_url =  self.strategy.restore(key)

        event = UrlRestored(long_url, short_url)
        self.event_handler.send_event(event)

        return long_url

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

