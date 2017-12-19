class Event(object):
    def __init__(self, long_url, short_url):
        self.long_url = long_url
        self.short_url = short_url

    def name(self):
        raise NotImplementedError()

    def payload(self):
        return { "long_url": self.long_url, "short_url": self.short_url }

class UrlMinified(Event):
    def name(self):
        return "url_minified"

class UrlRestored(Event):
    def name(self):
        return "url_restored"
