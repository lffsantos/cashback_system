#!/bin/bash
.PHONY: default
.SILENT:

migrate:
	python manage.py migrate --noinput

development:
	python manage.py runserver 0:8000

loaddata:
	python manage.py loaddata cashbackrange

test:
	pytest