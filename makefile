
setup:
	python -m venv ~/.flask-mobilenet-v3

source:
	. ~/.flask-mobilenet-v3

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

install-test:
	make install
	pip install -r requirements-test.txt

lint-force:
	isort .
	black .
	flake8 .
	pylint --disable=R,C,pointless-string-statement ./*.py ./tests

lint-check:
	isort . --check-only
	black --check .
	flake8 .
	pylint --disable=R,C,pointless-string-statement ./*.py ./tests

test:
	coverage run -m pytest -vv ./tests
	coverage report -m

docker-build:
	docker build -t mnv3 .

docker-push:
	docker push mnv3:latest

docker-run:
	docker run -d --name mnv3_app -p 80:8000 mnv3

docker-poll:
	docker ps --format "table {{.Image}}\t{{.Status}}\t{{.Names}}\t{{.Ports}}"
