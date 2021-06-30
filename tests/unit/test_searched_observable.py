import json
import pytest
from .resources import searched_observable
from trustar2.models.searched_observable import SearchedObservable


VALUE = "2.2.2.2"
TYPE = "IP4"
FIRST_SEEN = 1623273177255
LAST_SEEN = 1623701072520
ENCLAVE_GUIDS = ["test-enclave-guid"]
TAGS = ["test-tag"]



@pytest.fixture
def searched_observable_json():
    return json.loads(searched_observable)


@pytest.fixture
def searched_observable_obj():
    return SearchedObservable(
        value=VALUE,
        type=TYPE,
        first_seen=FIRST_SEEN,
        last_seen=LAST_SEEN,
        enclave_guids=ENCLAVE_GUIDS,
        tags=TAGS
    )


def test_searched_observable_deserialization(searched_observable_json):
    searched_observable = SearchedObservable.from_dict(searched_observable_json)

    assert searched_observable.value == VALUE
    assert searched_observable.type == TYPE
    assert searched_observable.first_seen == FIRST_SEEN
    assert searched_observable.last_seen == LAST_SEEN
    assert searched_observable.enclave_guids == ENCLAVE_GUIDS
    assert searched_observable.tags == TAGS


def test_searched_observable_serialization(searched_observable_obj, searched_observable_json):
    assert searched_observable_obj.serialize() == searched_observable_json
