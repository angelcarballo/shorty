# Shorty: fancy url shortener

Shorty is a demo URL shortener supporting different strategies for shortening urls and
persisting data.

Note: only in-memory persistence and persisted key strategies are implemented.

## Requirements

Shorty requires **Python3** and [ **pipenv** ](https://github.com/pypa/pipenv)

## Quick start

```sh
# install dependencies
> make init

# run test server
> make server

# create a user with a secure token
> curl -X POST http://127.0.0.1:5000/users -F email=test@test.com
{
  "email": "test@test.com",
  "secure_token": "XXXXXXXX"
}
```

## Test server API

Basic HTTP Authentication can be provided using email and secure token.

### POST /minify

 - Param `url` containing the long url is required.
 - Generates a short url that can be used to restore the original long url.
 - Requires basic HTTP Authentication.

### GET /restore

 - Param `url` containing the short url is required.
 - Returns the original long url for the provided short one.

### GET /stats

 - Param `url` containing the short url (optional)
 - If url is provided, return information about the given short url
 - If url is not provided, return information all urls created by the user
 - Requires basic HTTP Authentication.

### POST /users

 - Param `email` with the user's email is required.
 - Returns email and secure token for the new user.



 [![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/1617b072c4d5b107258f)

## Running tests

```sh
make test
```
