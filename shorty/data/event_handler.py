import time

from shorty.data.streamer import Streamer

class EventHandler(object):
    def __init__(self, streamer=Streamer()):
        self.streamer = streamer

    def send_event(self, event):
        timestamp = time.time()
        self.streamer.publish(timestamp, event.name(), event.payload())

