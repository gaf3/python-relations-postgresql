ACCOUNT=gaf3
IMAGE=relations-postgresql
INSTALL=python:3.8.5-alpine3.12
VERSION?=0.1.0
NETWORK=relations.io
POSTGRES_IMAGE=postgres:12.4-alpine
POSTGRES_HOST=$(ACCOUNT)-$(IMAGE)-postgres
DEBUG_PORT=5678
TTY=$(shell if tty -s; then echo "-it"; fi)
VOLUMES=-v ${PWD}/lib:/opt/service/lib \
		-v ${PWD}/test:/opt/service/test \
		-v ${PWD}/postgres.sh:/opt/service/postgres.sh \
		-v ${PWD}/.pylintrc:/opt/service/.pylintrc \
		-v ${PWD}/setup.py:/opt/service/setup.py
ENVIRONMENT=-e POSTGRES_HOST=$(POSTGRES_HOST) \
			-e POSTGRES_PORT=5432 \
			-e PYTHONDONTWRITEBYTECODE=1 \
			-e PYTHONUNBUFFERED=1 \
			-e test="python -m unittest -v" \
			-e debug="python -m ptvsd --host 0.0.0.0 --port 5678 --wait -m unittest -v"
.PHONY: build network postgres shell debug test lint setup tag untag

build:
	docker build . -t $(ACCOUNT)/$(IMAGE):$(VERSION)

network:
	-docker network create $(NETWORK)

postgres: network
	-docker rm --force $(POSTGRES_HOST)
	docker run -d --network=$(NETWORK) -h $(POSTGRES_HOST) --name=$(POSTGRES_HOST) -e POSTGRES_HOST_AUTH_METHOD='trust' $(POSTGRES_IMAGE)
	docker run $(TTY) --rm --network=$(NETWORK) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "./postgres.sh"

shell: postgres
	docker run $(TTY) --network=$(NETWORK) $(VOLUMES) $(ENVIRONMENT) -p 127.0.0.1:$(DEBUG_PORT):5678 $(ACCOUNT)/$(IMAGE):$(VERSION) sh

debug: postgres
	docker run $(TTY) --network=$(NETWORK) $(VOLUMES) $(ENVIRONMENT) -p 127.0.0.1:$(DEBUG_PORT):5678 $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "python -m ptvsd --host 0.0.0.0 --port 5678 --wait -m unittest discover -v test"

test: postgres
	docker run $(TTY) --network=$(NETWORK) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "coverage run -m unittest discover -v test && coverage report -m --include 'lib/*.py'"

lint:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "pylint --rcfile=.pylintrc lib/"

setup:
	docker run $(TTY) $(VOLUMES) $(INSTALL) sh -c "cp -r /opt/service /opt/install && cd /opt/install/ && \
	apk update && apk add git && \
	pip install git+https://github.com/gaf3/python-relations.git@5a19bb2#egg=relations && \
	pip install git+https://github.com/gaf3/python-relations-sql.git@57f5971#egg=relations-sql && \
	python setup.py install && \
	python -m relations_postgresql.sql && \
	python -m relations_postgresql.expression && \
	python -m relations_postgresql.criterion && \
	python -m relations_postgresql.criteria && \
	python -m relations_postgresql.clause && \
	python -m relations_postgresql.query && \
	python -m relations_postgresql.ddl && \
	python -m relations_postgresql.column && \
	python -m relations_postgresql.index && \
	python -m relations_postgresql.table"

tag:
	-git tag -a $(VERSION) -m "Version $(VERSION)"
	git push origin --tags

untag:
	-git tag -d $(VERSION)
	git push origin ":refs/tags/$(VERSION)"
