init:
	pipenv install

test:
	pipenv run pytest

server:
	FLASK_APP=server.py pipenv run flask run

dynamodb:
	mkdir -p vendor/dynamodb
	curl https://s3.eu-central-1.amazonaws.com/dynamodb-local-frankfurt/dynamodb_local_latest.tar.gz > vendor/dynamodb/dynamodb_local_latest.tar.gz
	cd vendor/dynamodb && tar xvfz dynamodb_local_latest.tar.gz

db:
	java -Djava.library.path=./vendor/dynamodb/DynamoDBLocal_lib -jar ./vendor/dynamodb/DynamoDBLocal.jar -sharedDb -dbPath ./db

.PHONY: init test server db
