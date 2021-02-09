[ad_keycloak](https://git.ucb.local/projects/AD/repos/ad_keycloak) is a library providing a python api to the Keycloak.

Developed by
[python 3.8](https://www.python.org) 
and
[aiohttp 3.7](https://aiohttp.readthedocs.io/en/stable)

## Requirements

* [Python 3.8](https://www.python.org/downloads/release/python-387/)
* [Poetry 1.1.3](https://python-poetry.org/)
* [Make](https://www.gnu.org/software/make/)

## Poetry

It is a dependency manager for Python. It aims to:

+ solve correlation problems of dependencies in different packages;
+ automatically creation of virtual environment;
+ easy package splitting into groups.

[Poetry](https://python-poetry.org/docs/) uses next files:
 
+ [pyproject.toml](https://python-poetry.org/docs/pyproject/) in witch we
describe information about service, dependencies and settings for other utils. 
+ `poetry.toml` in witch we set up Poetry configuration for the current project;
+ `poetry.lock` which Poetry create once at the first [install](https://python-poetry.org/docs/cli/#install)
command and write there package versions which was installed. Then Poetry use it despite
[pyproject.toml](https://python-poetry.org/docs/pyproject/) when you run 
[install](https://python-poetry.org/docs/cli/#install) again.

## Installation

To create [virtual environment](https://docs.python.org/3.7/library/venv.html) and install all dependencies run:

```bash
make setup
```

To make sure that all dependencies are installed, run the tests:

```bash
make test
```

If you want to update dependency versions you must run:

```bash
make update
```

## Tests

Run unit-tests:

```bash
make test
```

Run unit-tests with code coverage:

```bash
make cov
```

Test coverage reports will be located in the `.reports/coverage` folder.

## Checking

We use linters to check the written code:

[pylint](https://www.pylint.org/) (static code analysis tool):

```bash
make pylint
```

[mypy](http://mypy-lang.org/) (static type checker):

```bash
make mypy
```

[flake8](http://flake8.pycqa.org/en/latest/) (style guide enforcement tool):

```bash
make flake
```

To run all linter commands use the shortcut:

```bash
make lint
```

## Formatting

[isort](https://github.com/timothycrosley/isort) (A tool  add trailing commas to calls and literals):

```bash
make trailing
```

[add-trailing-comma](https://github.com/asottile/add-trailing-comma) (utility to sort imports):

```bash
make isort
```

To run all format commands use the shortcut:

```bash
make format
```


## Links
- [Git](https://git.ucb.local/projects/AD/repos/ad_client)
- [Jira](https://jira.ucb.local/browse/ALP-64)
- [Bamboo](https://bamboo.ucb.local/browse/AD-UTAC)
