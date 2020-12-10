# trustar-sdk2-proto

# Project development setup

This repository is built using tox to test the code with diferrent python versions. If you want to set up your development environment follow the instructions.

1.

If you don't have tox installed in your sysem

`pip install tox`

2.

`tox --devenv <virtualenv_name> -e <python_environment>`

Where virtualenv_name is the name you choose for your virtual environment and python_environment is one of the supported python version `py27` or `py37`.

### Example:

`tox --devenv .venv-py37 -e py37`

3.

Activate your virtual environment:

`source .venv-py37/bin/activate`

# Running tests

If you want to test all available environments:, just do:

`tox` in project's root

If you want to run an especific environment:

`tox -e py27` or `tox -e py37`
