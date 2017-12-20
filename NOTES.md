# Notes

## Shortening URLs

### Persistent key (implemented)

To meet the key length requirements, generating a random key seemed like the
simplest approach.

Small random keys will eventually generate collisions, regardless of the
algorithm used. With that in mind, I based the keys on the current timestamp,
which is probably the simplest approach. Collisions can be handled by adding
retries to the minify process.

### Compression (not implemented)

Using compression suitable for small strings seems like a better, more
functional approach with no need for a database to persist the generated
keys. It would not support _custom keys_ though, but those could be generated
using a persisted key as a fallback strategy.

The main disadvantage of this approach is that it will generate slightly longer
keys for long urls. In the available libraries (like
[shoco](https://ed-von-schleck.github.io/shoco/)), it seems this can be improved
with custom dictionaries

## Scaling

At the moment the endpoint is using a demo HTTP endpoint, but this application
is a great candidate for a serverless setup using AWS Lambda+DynamoDB or a similar
service.

Not requiring a database, an approach using compression strategy would be even
easier to scale.

## Data

All data is collected from events. In the demo app, a dummy streamer stores the
events in memory and provides rudimentary methods to query them. On a real
application, the different event would be streamed via AWS Kinesis (or Kafka).

Information generated from those events should be stored separately and consumed
via a different service.

The main choice here is to keep all data responsibilities out of the main
application, which only needs to fire and forget the right events.

## Wish list

 - The implemented authentication is a joke. I wanted JSON Web Tokens, but time...
 - Needs more tests, and the ones covering `UrlMinifier` would be more valuable
   on a Cucumber feature.
 - Missing deployment. As mentioned, this could be a great fit for
   Lambda/DynamoDB/Kinesis/API Gateway, but time...
 - Implement compression strategy
 - Implement persistence with a real db

