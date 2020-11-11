import pytest

from trustar.indicators import SearchIndicator


@pytest.fixture
def search_indicator():
    search_indicator = SearchIndicator(None) # update to use dummy config
    return search_indicator


def test_search_indicators_is_empty(search_indicator):
    assert len(search_indicator.params) == 0


def test_set_query_term(search_indicator):
    search_indicator.set_query_term("TEST_TERM")
    values = [param.value for param in search_indicator.params]
    assert len(search_indicator.params) == 1
    assert values[0] == "TEST_TERM"


@pytest.mark.parametrize("from_date", [1596607968000, "2020-11-08", "3 months ago"])
def test_set_from(search_indicator, from_date):
    if not isinstance(from_date, int):
        timestamp = search_indicator._get_timestamp(from_date)
    else:
        timestamp = from_date

    search_indicator.set_from(from_date)
    values = [param.value for param in search_indicator.params]
    assert len(search_indicator.params) == 1
    assert values[0] == timestamp


@pytest.mark.parametrize("to_date", [1596607968000, "2020-11-10", "1 day ago"])
def test_set_to(search_indicator, to_date):
    if not isinstance(to_date, int):
        timestamp = search_indicator._get_timestamp(to_date)
    else:
        timestamp = to_date

    search_indicator.set_to(to_date)
    values = [param.value for param in search_indicator.params]
    assert len(search_indicator.params) == 1
    assert values[0] == timestamp


@pytest.mark.parametrize("column", [
    "UPDATED", 
    pytest.param("INVALID", marks=pytest.mark.xfail(raises=AttributeError))
])
def test_set_sort_column(search_indicator, column):
    search_indicator.set_sort_column(column)
    values = [param.value for param in search_indicator.params]
    assert len(search_indicator.params) == 1
    assert values[0] == column


@pytest.mark.parametrize("scores", [
    [1,2,3],
    pytest.param([1,2,4], marks=pytest.mark.xfail(raises=AttributeError))
])
def test_set_priority_scores(search_indicator, scores):
    search_indicator.set_priority_scores(scores)
    values = [param.value for param in search_indicator.params]
    assert len(search_indicator.params) == 1
    assert values[0] == scores


def test_set_enclave_ids(search_indicator):
    search_indicator.set_enclave_ids(["TEST_ENCLAVE_ID"])
    values = [param.value for param in search_indicator.params]
    assert len(search_indicator.params) == 1
    assert values[0] == ["TEST_ENCLAVE_ID"]


@pytest.mark.parametrize("obs_types", [
    ["URL", "MD5", "IP4"],
    pytest.param(["INVALID", "URL"], marks=pytest.mark.xfail(raises=AttributeError))
])
def test_set_observable_types(search_indicator, obs_types):
    search_indicator.set_observable_types(obs_types)
    values = [param.value for param in search_indicator.params]
    assert len(search_indicator.params) == 1
    assert values[0] == obs_types


@pytest.mark.parametrize("attributes", [
    [{"type": "MALWARE", "value": "ATTRIBUTE"}],
    pytest.param(
        [{"type": "INVALID", "value": "ATTRIBUTE"}], 
        marks=pytest.mark.xfail(raises=AttributeError))
])
def test_set_attributes(search_indicator, attributes):
    search_indicator.set_attributes(attributes)
    values = [param.value for param in search_indicator.params]
    assert len(search_indicator.params) == 1
    assert values[0] == attributes


@pytest.mark.parametrize("observables", [
    [{"type": "URL", "value": "RELATED_OBS"}],
    pytest.param(
        [{"type": "INVALID", "value": "RELATED_OBS"}], 
        marks=pytest.mark.xfail(raises=AttributeError))
])
def test_set_related_observable(search_indicator, observables):
    search_indicator.set_related_observables(observables)
    values = [param.value for param in search_indicator.params]
    assert len(search_indicator.params) == 1
    assert values[0] == observables


def test_set_duplicated_query_terms(search_indicator):
    search_indicator.set_query_term("TEST_TERM")
    search_indicator.set_query_term("TEST_TERM2")
    values = [param.value for param in search_indicator.params]
    assert len(search_indicator.params) == 1
    assert values[0] == "TEST_TERM"

 
@pytest.mark.xfail(raises=AttributeError)
def test_query_will_not_work_due_to_invalid_dates(search_indicator):
    search_indicator.set_from("1 day ago")
    search_indicator.set_to("2 days ago")
    search_indicator.query()
