# TruSTAR SDK 2

# Documentation

Click [here](documentation.md) to check some examples of how the SDK is used and the data model.

# Project development setup

This repository is built using tox to test the code with diferrent python versions. If you want to set up your development environment follow the instructions.

1. If you don't have tox installed in your system, do the following:

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

If you want to run a specific environment:

`tox -e py27` or `tox -e py37`

# Releasing a new version

To publish a new version in PyPI you should use the `release.sh` script that is in the root of the project. Suppose you want to release v0.0.1, you should do:

```
bash release.sh v0.0.1
```

Obviously, in order to make a release, you must have permissions to do so and you must have your PyPI creds available for Twine.
