all:

.PHONY: install
install:
	pip install -e .

.PHONY: develop
develop: install
	pip install flake8

.PHONY: flake8
flake8:
	flake8 django_compose_settings tests

.PHONY: tests
tests:
	python -m unittest discover -v tests/

.PHONY: release
release:
	pip install -e ".[release]"
	fullrelease
