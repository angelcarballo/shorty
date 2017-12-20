import time

from shorty.data.streamer import Streamer

class EventHandler(object):
    """ Handler used to send events to a stream """

    def __init__(self, streamer=Streamer()):
        self.streamer = streamer

    def send_event(self, event):
        timestamp = time.time()
        self.streamer.publish(timestamp, event.name(), event.payload())

