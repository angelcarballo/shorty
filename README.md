# Shorty: fancy url shortener

Shorty is a demo URL shortener supporting different strategies for shortening urls and
persisting data.

Note: only in-memory persistence and persisted key strategies are implemented.

## Requirements

Shorty requires **Python3** and [ **pipenv** ](https://github.com/pypa/pipenv)

## Quick start

```sh
# install dependencies
make init

# run test server
make server

# tail the logs to monitor events being fired
tail -f events.log | grep root

# create a user with a secure token,
# the response will include email and secure_token
#  example: { "email": "test@test.com", "secure_token": "XXXXXXXX" }
curl -X POST http://127.0.0.1:5000/users -F email=test@test.com

# shorten a url (authorization header generated from email/secure_token)
curl -X POST http://127.0.0.1:5000/minify \
  -H 'authorization: Basic XXXXXXXXXXXXX' \
  -F url=https://en.wikipedia.org/wiki/Foobar/this/url/is/too/large \
  -F key=mykey

# restore the original url
curl -X GET 'http://127.0.0.1:5000/restore?url=http%3A%2F%2Fshor.ty%2F%2Fmykey'

# get stats for the url (authorization header generated from email/secure_token)
curl -X GET 'http://127.0.0.1:5000/stats?url=http%3A%2F%2Fshor.ty%2F%2Fmykey' \
  -H 'authorization: Basic XXXXXXXXXXXXX'

# get full stats
curl -X GET http://127.0.0.1:5000/stats \
  -H 'authorization: Basic XXXXXXXXXXXXX'

```

## Test server API

Basic HTTP Authentication can be provided using email and secure token.

### POST /minify

 - Param `url` containing the long url is required
 - Generates a short url that can be used to restore the original long url
 - Requires basic HTTP Authentication

### GET /restore

 - Param `url` containing the short url is required
 - Returns the original long url for the provided short one

### GET /stats

 - Param `url` containing the short url (optional)
 - If url is not provided, returns statistics about all the urls created by the user
 - If a url is provided, returns only statistics for that url
 - Requires basic HTTP Authentication

### POST /users

 - Param `email` with the user's email is required
 - Returns email and secure token for the new user



 [![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/1617b072c4d5b107258f)

## Running tests

```sh
make test
```
