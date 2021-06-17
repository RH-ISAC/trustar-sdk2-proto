import pytest
import requests_mock

from trustar2.trustar import TruStar

API_VERSION = "2.0{}"
BASE_URL = "https://api.trustar.co/api/{}".format(API_VERSION)


@pytest.fixture
def mocked_request():
    with requests_mock.Mocker() as m:
        m.post(url="/oauth/token", text='{"access_token": "TOKEN12345"}')
        yield m
