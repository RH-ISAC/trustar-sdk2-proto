from __future__ import unicode_literals

import json
import pytest

from trustar2 import Account, TruStar
from tests.unit.resources import enclaves


URL = "https://api.trustar.co/api/2.0"


@pytest.fixture
def account():
    return Account(
        TruStar(api_key="xxxx", api_secret="xxx", client_metatag="test_env")
    )


@pytest.fixture
def enclaves_response():
    return json.loads(enclaves)


def test_ping_successfully(account, mocked_request):
    mocked_request.get(URL + "/ping", status_code=200, text="pong\n")
    response = account.ping()
    assert response.status_code == 200
    assert response.text == "pong\n"


def test_get_enclaves_successfully(account, mocked_request, enclaves_response):
    mocked_request.get(URL + "/enclaves", json=enclaves_response)
    response = account.get_enclaves()
    assert response.status_code == 200
    assert response.json() == enclaves_response
