PROJECT := ad_keycloak
VERSION := $(shell git describe --tags `git rev-list --tags --max-count=1`)

VENV := .venv
export PATH := $(VENV)/bin:$(PATH)

REPORTS := .reports
COVERAGE := $(REPORTS)/coverage

SOURCES := $(PROJECT)
TESTS := tests

PY_FILES = $(shell find $(SOURCES) $(TESTS) -name "*.py")

clean:
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf $(REPORTS)
	rm -rf $(VENV)

$(VENV):
	poetry install --no-root --extras pytest-plugin

$(REPORTS):
	mkdir $(REPORTS)

setup: $(VENV) $(REPORTS)

update: setup
	poetry update

mypy: setup
	mypy $(SOURCES) $(TESTS)

pylint: setup
	pylint $(SOURCES) $(TESTS) > $(REPORTS)/pylint.txt

flake: setup
	flake8 $(SOURCES) $(TESTS)

bandit: setup
	bandit -f json -o $(REPORTS)/bandit.json -r $(SOURCES) $(TESTS) -s B101

isort: setup  # TODO: tralling
	isort $(SOURCES) $(TESTS)

isort-lint: setup
	isort -c $(SOURCES) $(TESTS)

trailing: setup
	@add-trailing-comma $(PY_FILES) --py36-plus --exit-zero-even-if-changed

trailing-lint: setup
	@add-trailing-comma $(PY_FILES) --py36-plus

test: setup
	pytest --junitxml=$(REPORTS)/junit.xml

cov: setup
	coverage run --source $(PROJECT) --module pytest
	coverage report
	coverage html -d $(COVERAGE)/html
	coverage xml -o $(COVERAGE)/cobertura.xml
	coverage erase
	cobertura-clover-transform $(COVERAGE)/cobertura.xml -o $(COVERAGE)/clover.xml

lint: isort-lint trailing-lint mypy pylint flake bandit

format: isort trailing

all: format lint cov

.DEFAULT_GOAL := all
