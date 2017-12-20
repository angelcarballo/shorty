from flask import Flask, request, abort, jsonify, session
from flask_httpauth import HTTPBasicAuth

from shorty.urlminifier import UrlMinifier
from shorty.strategy.persisted_key import PersistedKey
from shorty.data.event_handler import EventHandler
from shorty.data.streamer import Streamer
from shorty.db.memory import Memory
from shorty.user import User

app = Flask(__name__)
app.secret_key = 'this-should-not-be-here'
auth = HTTPBasicAuth()

max_key_len = 23 - len('http://shor.ty/')

db = Memory()
strategy = PersistedKey(max_len=max_key_len, db=db)
streamer = Streamer()
event_handler = EventHandler(streamer=streamer)

url_minifier = UrlMinifier(domain="http://shor.ty",
                           strategy=strategy,
                           event_handler=event_handler)

@auth.get_password
def get_user_token(email):
    try:
        user = db.get_user(email)
        session["user_id"] = user.email
        return user.secure_token
    except KeyError:
        return None

@app.route("/minify", methods=['POST'])
@auth.login_required
def minify():
    long_url = request.form.get('url')
    key = request.form.get('key')
    if not long_url: abort(422)

    short_url = url_minifier.minify(long_url,
                                    session.get("user_id"),
                                    requested_key=key)
    return jsonify({"short_url": short_url})

@app.route("/restore")
def restore():
    short_url = request.args.get('url')
    if not short_url: abort(422)

    long_url = url_minifier.restore(short_url)
    return jsonify({"long_url": long_url})

@app.route("/stats")
@auth.login_required
def stats():
    short_url = request.args.get('url')
    if short_url:
        stats = streamer.short_url_stats(short_url)
    else:
        stats = streamer.user_stats(session.get("user_id"))
    return jsonify(stats)

@app.route("/users", methods=["POST"])
def create_user():
    email = request.form.get("email")
    if not email: abort(422)
    user = User(email)
    db.store_user(user)
    return jsonify({"email": user.email, "secure_token": user.secure_token})
