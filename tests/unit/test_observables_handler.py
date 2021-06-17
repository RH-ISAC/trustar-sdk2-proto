from __future__ import unicode_literals
import json
from .resources import observables_search_example_request
from trustar2.handlers.observables import ObservablesHandler
from trustar2.handlers.tags import TagObservable
import pytest


TEST_DATE = [1583960400000, "2020-03-11T21:00:00"]

@pytest.fixture
def observables_handler(ts):
    return ObservablesHandler(ts)

def test_set_search_types_valid(observables_handler):
    assert len(observables_handler.payload_params) == 0
    types = ["MD5", "SOFTWARE"]
    observables_handler.set_search_types(types)
    assert len(observables_handler.payload_params) == 1
    assert sorted(observables_handler.payload_params.get("types")) == types

def test_set_search_types_invalid(observables_handler):
    assert len(observables_handler.payload_params) == 0
    types = ["INVALID_TYPE", "MD5"]
    with pytest.raises(AttributeError):
        observables_handler.set_search_types(types)
    assert len(observables_handler.payload_params) == 0

def test_set_sort_column_valid(observables_handler):
    assert len(observables_handler.payload_params) == 0
    observables_handler.set_sort_column("FIRST_SEEN")
    assert observables_handler.payload_params.get("sortColumn") == "FIRST_SEEN"
    assert len(observables_handler.payload_params) == 1
    observables_handler.set_sort_column("LAST_SEEN")
    assert observables_handler.payload_params.get("sortColumn") == "LAST_SEEN"
    assert len(observables_handler.payload_params) == 1

def test_set_sort_column_vinalid(observables_handler):
    assert len(observables_handler.payload_params) == 0
    with pytest.raises(AttributeError):
        observables_handler.set_sort_column("UPDATED")
    assert len(observables_handler.payload_params) == 0

def tags(observables_handler):
    tags = observables_handler.tags()
    assert(isinstance(tags, TagObservable))

def test_search_too_many_included_tags(observables_handler):
    MAX_TAGS = 20
    tags = list(range(0, MAX_TAGS + 1))
    observables_handler.set_included_tags(tags)
    with pytest.raises(AttributeError):
        observables_handler.search()

def test_search_too_many_excluded_tags(observables_handler):
    MAX_TAGS = 20
    tags = list(range(0, MAX_TAGS + 1))
    observables_handler.set_excluded_tags(tags)
    with pytest.raises(AttributeError):
        observables_handler.search()


def test_search_invalid_dates(observables_handler):
    observables_handler.set_from("1 day ago")
    observables_handler.set_to("2 days ago")
    with pytest.raises(AttributeError):
        observables_handler.search()

def test_search(observables_handler):
    types = ["MD5"]
    query_term = "query"
    enclave_ids = ["4bdc3f5b-3ed5-4d99-b20c-2d801866ef0b"]
    from_date = 1596607968000
    to_date = 1598308171000

    q = (
        observables_handler.set_query_term(query_term)
        .set_enclave_ids(enclave_ids)
        .set_search_types(types)
        .set_from(from_date)
        .set_to(to_date)
        .set_sort_column("FIRST_SEEN")
        .set_sort_order("ASC")
        .search()
    )
    assert q.params.serialize() == json.loads(observables_search_example_request)

def test_get_from_submission(observables_handler):
    submission_id = "2d87abca-3b6c-4bdc-b9dd-0a3e29901bbb"
    q = observables_handler.get_from_submission(submission_id)
    assert(q.query_string.get("submissionId") ==  submission_id)    