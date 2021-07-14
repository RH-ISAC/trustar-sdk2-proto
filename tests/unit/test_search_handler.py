from __future__ import unicode_literals

from trustar2.trustar_enums import TSEnum
from trustar2.handlers.search_handler import SearchHandler
import pytest


TEST_DATE = [1583960400000, "2020-03-11T21:00:00"]

@pytest.fixture
def search_handler(ts):
    return SearchHandler(ts)

def test_set_query_term(search_handler):
    assert len(search_handler.payload_params) == 0
    search_handler.set_query_term("TEST_TERM")
    values = [param.value for param in search_handler.payload_params]
    assert len(search_handler.payload_params) == 1
    assert values[0] == "TEST_TERM"


def test_override_query_term(search_handler):
    assert len(search_handler.payload_params) == 0
    search_handler.set_query_term("TEST_TERM1")
    assert search_handler.payload_params.get("queryTerm") == "TEST_TERM1"
    assert len(search_handler.payload_params) == 1
    search_handler.set_query_term("TEST_TERM2")
    assert len(search_handler.payload_params) == 1
    assert search_handler.payload_params.get("queryTerm") == "TEST_TERM2"

@pytest.mark.parametrize("from_date", TEST_DATE)
def test_set_from(search_handler, from_date):
    assert len(search_handler.payload_params) == 0
    search_handler.set_from(from_date)
    assert search_handler.payload_params.get("from") == TEST_DATE[0]
    assert len(search_handler.payload_params) == 1


def test_set_from_fail(search_handler):
    assert len(search_handler.payload_params) == 0
    with pytest.raises(TypeError):
        search_handler.set_from("XXXX-XX-XX")
    assert len(search_handler.payload_params) == 0


def test_invalid_dates(search_handler):
    search_handler.set_from("1 day ago")
    search_handler.set_to("2 days ago")
    with pytest.raises(AttributeError):
        search_handler._validate_dates()


@pytest.mark.parametrize("to_date", TEST_DATE)
def test_set_to(search_handler, to_date):
    assert len(search_handler.payload_params) == 0
    search_handler.set_to(to_date)
    assert search_handler.payload_params.get("to") == TEST_DATE[0]
    assert len(search_handler.payload_params) == 1


def test_set_to_fail(search_handler):
    assert len(search_handler.payload_params) == 0
    with pytest.raises(TypeError):
        search_handler.set_to("XXXX-XX-XX")
    assert len(search_handler.payload_params) == 0


def test_set_enclave_ids(search_handler):
    assert len(search_handler.payload_params) == 0
    search_handler.set_enclave_ids(["TEST_ENCLAVE_ID"])
    assert len(search_handler.payload_params) == 1
    assert search_handler.payload_params.get("enclaveGuids") == ["TEST_ENCLAVE_ID"]

def test_set_enclave_ids_single_value(search_handler):
    assert len(search_handler.payload_params) == 0
    search_handler.set_enclave_ids("TEST_ENCLAVE_ID")
    assert len(search_handler.payload_params) == 1
    assert search_handler.payload_params.get("enclaveGuids") == ["TEST_ENCLAVE_ID"]

def test_set_included_tags(search_handler):
    assert len(search_handler.payload_params) == 0
    search_handler.set_included_tags(["test-tag"])
    assert len(search_handler.payload_params) == 1
    assert search_handler.payload_params.get("includedTags") == ["test-tag"]

def test_set_included_tags_repeated_values(search_handler):
    tags = ['a', 'b', 'c', 'a' , 'b' , 'd']
    expected_tags = ['a', 'b', 'c', 'd']
    assert len(search_handler.payload_params) == 0
    search_handler.set_included_tags(tags)
    assert(len(search_handler.payload_params)) == 1
    assert(sorted(search_handler.payload_params.get("includedTags"))) == expected_tags

def test_set_excluded_tags(search_handler):
    assert len(search_handler.payload_params) == 0
    search_handler.set_excluded_tags(["test-tag"])
    assert len(search_handler.payload_params) == 1
    assert search_handler.payload_params.get("excludedTags") == ["test-tag"]

def test_set_excluded_tags_repeated_values(search_handler):
    tags = ['a', 'b', 'c', 'a' , 'b' , 'd']
    expected_tags = ['a', 'b', 'c', 'd']
    assert len(search_handler.payload_params) == 0
    search_handler.set_excluded_tags(tags)
    assert(len(search_handler.payload_params)) == 1
    assert(sorted(search_handler.payload_params.get("excludedTags"))) == expected_tags

def test_set_sort_column_with_default_options(search_handler):
    assert len(search_handler.payload_params) == 0
    search_handler.set_sort_column("UPDATED")
    assert len(search_handler.payload_params) == 1
    assert search_handler.payload_params.get("sortColumn") == "UPDATED"

def test_set_sort_column_with_invalid_options(search_handler):
    class Options(TSEnum):
        OPT = "OPT"
    assert len(search_handler.payload_params) == 0
    with pytest.raises(AttributeError):
        search_handler.set_sort_column("UPDATED", Options)
    assert len(search_handler.payload_params) == 0

def test_set_sort_column_with_valid_options(search_handler):
    class Options(TSEnum):
        OPT = "OPT"
    assert len(search_handler.payload_params) == 0
    search_handler.set_sort_column("OPT", Options)
    assert len(search_handler.payload_params) == 1
    assert search_handler.payload_params.get("sortColumn") == "OPT"

def test_set_sort_order_with_valid_options(search_handler):
    assert len(search_handler.payload_params) == 0
    search_handler.set_sort_order("ASC")
    assert len(search_handler.payload_params) == 1
    assert search_handler.payload_params.get("sortOrder") == "ASC"
    search_handler.set_sort_order("DESC")
    assert len(search_handler.payload_params) == 1
    assert search_handler.payload_params.get("sortOrder") == "DESC"

def test_set_sort_order_with_invalid_options(search_handler):
    assert len(search_handler.payload_params) == 0
    with pytest.raises(AttributeError):
        search_handler.set_sort_order("ASCC")
    assert len(search_handler.payload_params) == 0


def test_set_page_size(search_handler):
    assert len(search_handler.query_params) == 0
    search_handler.set_page_size(999)
    assert len(search_handler.query_params) == 1
    assert search_handler.query_params.get("pageSize") == 999
