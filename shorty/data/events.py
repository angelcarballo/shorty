class UrlMinified(object):
    def __init__(self, long_url, short_url, user_id):
        self.long_url = long_url
        self.short_url = short_url
        self.user_id = user_id

    def name(self):
        return "url_minified"

    def payload(self):
        return {
            "long_url": self.long_url,
            "short_url": self.short_url,
            "user_id": self.user_id
        }

class UrlRestored(object):
    def __init__(self, long_url, short_url):
        self.long_url = long_url
        self.short_url = short_url

    def name(self):
        return "url_restored"

    def payload(self):
        return { "long_url": self.long_url, "short_url": self.short_url }

