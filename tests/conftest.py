import pytest
import requests_mock

from trustar2.trustar import TruStar

BASE_API = "https://api.trustar.co/api/{}"
BASE_URL = BASE_API.format("2.0{}")


@pytest.fixture
def mocked_request():
    with requests_mock.Mocker() as m:
        m.post(url="/oauth/token", text='{"access_token": "TOKEN12345"}')
        yield m
