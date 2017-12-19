init:
	pipenv install

test:
	pipenv run pytest

server:
	FLASK_APP=server.py pipenv run flask run

.PHONY: init test server
