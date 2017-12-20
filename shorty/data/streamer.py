import logging
import json
import datetime

logging.basicConfig(filename="events.log", level=logging.DEBUG)

class Streamer(object):
    def __init__(self):
        self.events = []

    def publish(self, timestamp, event, payload):
        event = {
            "timestamp": timestamp,
            "event": event
        }
        payload.update(event)
        self.events.append(payload)
        logging.info(json.dumps(payload))

    def short_url_stats(self, short_url):
        minify_info = self.minify_info(short_url)
        shortened_at = datetime.datetime.fromtimestamp(minify_info["timestamp"])
        return {
            "short_url": minify_info["short_url"],
            "long_url": minify_info["long_url"],
            "shortened_at": str(shortened_at),
            "access_count": self.restore_count(short_url)
        }

    def user_stats(self, user_id):
        user_urls = [e["short_url"] for e in self.events
                     if e.get("user_id") == user_id]
        stats = {
            "user_id": user_id,
            "urls": [self.short_url_stats(url) for url in user_urls]
        }
        return stats

    def minify_info(self, short_url):
        events = self.__events_for("url_minified", short_url)
        return events[0]

    def restore_count(self, short_url):
        return len(self.__events_for("url_restored", short_url))

    def __events_for(self, type, short_url):
        events = [e for e in self.events
                  if e["event"] == type and e["short_url"] == short_url]
        return events
