import pytest

from trustar2.api_client import ApiClient
from trustar2.trustar import TruStar
from trustar2.version import __version__


@pytest.fixture
def api_client():
    return ApiClient(TruStar("API_KEY", "API_SECRET", "TEST_METATAG"))


def test_get_token_successfully(api_client, mocked_request):
    token = api_client._get_token()
    assert token == "TOKEN12345"


def test_get_headers(api_client, mocked_request):
    headers = api_client._get_headers("POST")
    expected_headers = {
        "Authorization": "Bearer TOKEN12345",
        "Client-Metatag": "TEST_METATAG",
        "Client-Type": "PYTHON_SDK",
        "Client-Version": __version__,
        "Content-Type": "application/json",
    }
    assert headers == expected_headers


def test_token_is_not_expired(api_client, mocker):
    mock_response = mocker.Mock(status_code=200)
    expired = api_client._token_is_expired(mock_response)
    assert not expired


def test_token_is_expired(api_client, mocker):
    mock_response = mocker.Mock(
        status_code=400,
        json=lambda: {"error_description": "Expired oauth2 access token"},
    )
    expired = api_client._token_is_expired(mock_response)
    assert expired


def test_sleep_wait_time_lower_max_wait_time(api_client, mocker):
    mock_response = mocker.Mock(
        json=lambda: {"waitTime": 500},
    )
    keep_trying = api_client._sleep(mock_response)
    assert keep_trying


def test_sleep_wait_time_higher_max_wait_time(api_client, mocker):
    mock_response = mocker.Mock(
        json=lambda: {"waitTime": 65000},
    )
    keep_trying = api_client._sleep(mock_response)
    assert not keep_trying
