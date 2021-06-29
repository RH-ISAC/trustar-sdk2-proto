import json
import pytest
from .resources import searched_observable
from trustar2.models.searched_observable import SearchedObservable


@pytest.fixture
def searched_observable_json():
    return json.loads(searched_observable)


def test_searched_observable_deserialization(searched_observable_json):
    searched_observable = SearchedObservable.from_dict(searched_observable_json)

    assert searched_observable.value == "2.2.2.2"
    assert searched_observable.type == "IP4"
    assert searched_observable.first_seen == 1623273177255
    assert searched_observable.last_seen == 1623701072520
    assert searched_observable.enclave_guids == ["test-enclave-guid"]
