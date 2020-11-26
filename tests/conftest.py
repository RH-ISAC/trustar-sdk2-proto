import pytest
import requests_mock

from trustar.trustar import TruStar

BASE_URL = "/api/2.0"


@pytest.fixture
def mocked_request():
    with requests_mock.Mocker() as m:
        m.post(url="/oauth/token", text='{"access_token": "TOKEN12345"}')
        yield m
