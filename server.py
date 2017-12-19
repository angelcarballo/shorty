from flask import Flask, request, abort

from shorty.urlminifier import UrlMinifier
from shorty.strategy.persisted_key import PersistedKey

app = Flask(__name__)

max_key_len = 23 - len('http://shor.ty/')
strategy = PersistedKey(max_len=max_key_len)

url_minifier = UrlMinifier(domain="http://shor.ty", strategy=strategy)

@app.route("/minify", methods=['POST'])
def minify():
    long_url = request.form.get('url')
    key = request.form.get('key')
    if not long_url: abort(422)
    short_url = url_minifier.minify(long_url, requested_key=key)
    return short_url

@app.route("/restore")
def restore():
    short_url = request.args.get('url')
    if not short_url: abort(422)
    long_url = url_minifier.restore(short_url)
    return long_url
