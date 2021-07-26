import json

import pytest

from tests.unit.resources import searched_observable
from trustar2.models.searched_observable import SearchedObservable
from trustar2.trustar_enums import ObservableTypes

VALUE = "2.2.2.2"
TYPE = ObservableTypes.IP4.value
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


def test_searched_observable_repr(searched_observable_obj):
    assert searched_observable_obj.__repr__() == "SearchedObservable(type=IP4, value=2.2.2.2)"
