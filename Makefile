PYTHON := python
PIP := pip
PACKAGES := ctime

.PHONY: build install install-e test clean release
.DEFAULT_GOAL := help

help:
	@echo "Welcome to the CTime Makefile"
	@echo "Available commands:"
	@echo "  help       - Show this help message"
	@echo "  install    - Install the package"
	@echo "  install-e  - Install the package in development mode"
	@echo "  test       - Run the tests"
	@echo "  clean      - Clean the build and dist directories"
	@echo "  release    - Run on release"

install:
	$(PIP) install .

install-e:
	$(PIP) install -e .

test:
	$(PYTHON) -m unittest discover -s tests

clean:
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@rm -rf src
	@find . -type f -name "*.so" -delete

build:
	$(PYTHON) setup.py build_ext --inplace

release:
	make build install test