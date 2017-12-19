from flask import Flask, request, abort, jsonify

from shorty.urlminifier import UrlMinifier
from shorty.strategy.persisted_key import PersistedKey
from shorty.data.event_handler import EventHandler
from shorty.data.streamer import Streamer

app = Flask(__name__)

max_key_len = 23 - len('http://shor.ty/')

strategy = PersistedKey(max_len=max_key_len)
streamer = Streamer()
event_handler = EventHandler(streamer=streamer)

url_minifier = UrlMinifier(domain="http://shor.ty", strategy=strategy,
                           event_handler=event_handler)

@app.route("/minify", methods=['POST'])
def minify():
    long_url = request.form.get('url')
    key = request.form.get('key')
    if not long_url: abort(422)

    short_url = url_minifier.minify(long_url, requested_key=key)
    return jsonify({"short_url": short_url})

@app.route("/restore")
def restore():
    short_url = request.args.get('url')
    if not short_url: abort(422)

    long_url = url_minifier.restore(short_url)
    return jsonify({"long_url": long_url})

@app.route("/stats")
def stats():
    short_url = request.args.get('url')
    if not short_url: abort(422)
    stats = streamer.short_url_stats(short_url)
    return jsonify(stats)
