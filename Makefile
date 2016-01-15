all:

.PHONY: install
install:
	pip install -e .

.PHONY: develop
develop: install
	pip install flake8

.PHONY: tests
tests:
	flake8 .
	python -m unittest discover tests/

.PHONY: release
release:
	pip install -e ".[release]"
	fullrelease
