import pytest

from trustar2.trustar import TruStar

proxy = {"https": "https://user:pass@le.proxy.com", "http":None}


@pytest.fixture
def trustar_with_proxy():
    return TruStar(api_key="xxxx", api_secret="xxx", client_metatag="test_env", proxy=proxy)


@pytest.fixture
def trustar():
    return TruStar(api_key="xxxx", api_secret="xxx", client_metatag="test_env")


def test_trustar_proxy(trustar):
    assert trustar.get_proxy() == {}


def test_trustar_with_proxy(trustar_with_proxy):
    assert trustar_with_proxy.get_proxy() == {"https": "https://user:pass@le.proxy.com"}
