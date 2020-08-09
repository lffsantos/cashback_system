#!/bin/bash
.PHONY: default
.SILENT:


default:

_local_env:
	-cp -n local.env.sample local.env

bash: _local_env
	docker-compose stop django
	docker-compose run --rm --service-ports django bash

shell:
	docker-compose run --rm django python manage.py shell_plus

migrate: _local_env
	docker-compose run --rm django python manage.py migrate --noinput

start: migrate
	docker-compose up -d

stop: _local_env
	docker-compose down

development:
	docker-compose run --rm --service-ports django python manage.py runserver 0:8000

restart-celery:
	docker-compose restart celeryworker celerybeat celeryflower

logs:
	docker-compose logs --follow

clean-containers:
	-docker ps -aqf ancestor=api_* | xargs docker rm -f

clean-images:
	-docker images -q -f reference=api_* | xargs docker rmi -f

clean-volumes:
	-docker volume ls -q -f name=api_* | xargs docker volume rm -f

clean-layers:
	-docker images -q -f dangling=true | xargs docker rmi -f

clean-all: stop clean-containers clean-images clean-volumes clean-layers

createsuperuser:
	docker-compose run --rm django python manage.py createsuperuser --email admin@expeer.com.br

loaddata:
	docker-compose run --rm django python manage.py loaddata marketing groups banks monthlyincome reasoncancel totalequity social_auth

dependencies:
	docker-compose run --rm --no-deps django pip list --outdated format columns

# Code quality
# -----------------------------------------------------------------------------
test:
	docker-compose run --rm django pytest

codestyle:
	docker-compose run --rm --no-deps django pycodestyle . --exclude migrations

lint-django:
	docker-compose run --rm --no-deps django pylint --load-plugins pylint_django incorporators investors real_estates topazio users

continuous-integration:
	docker-compose --file docker-compose.ci.yml run --rm --no-deps django pip list --outdated --format columns
	docker-compose --file docker-compose.ci.yml run --rm --no-deps django pycodestyle . --exclude migrations
	docker-compose --file docker-compose.ci.yml run --rm django pytest --cov

# Build & Deploy
# -----------------------------------------------------------------------------
login:
	$$(aws ecr get-login --no-include-email)

build-development:
	docker-compose build --force-rm --no-cache --pull

build-staging:
	docker build -t staging .

build: build-development build-staging


push-staging: build-staging login
	docker tag staging:latest 585930739802.dkr.ecr.us-east-1.amazonaws.com/staging:latest
	docker push 585930739802.dkr.ecr.us-east-1.amazonaws.com/staging:latest
