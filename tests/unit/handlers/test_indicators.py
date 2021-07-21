from __future__ import unicode_literals

import json
import pytest

from trustar2.models import Entity
from trustar2 import SearchIndicator
from trustar2.trustar_enums import ObservableTypes
from tests.unit.resources import indicators_example_request


@pytest.fixture
def search_indicator(ts):
    return SearchIndicator(ts)


def test_search_indicators_is_empty(search_indicator):
    assert len(search_indicator.payload_params) == 0


def test_set_priority_scores(search_indicator):
    scores = [1, 2, 3]
    search_indicator.set_priority_scores(scores)
    assert len(search_indicator.payload_params) == 1
    assert search_indicator.payload_params.get("priorityScores") == scores


def test_set_priority_scores_fail(search_indicator):
    scores = [1, 2, 4]
    with pytest.raises(AttributeError):
        search_indicator.set_priority_scores(scores)
    assert len(search_indicator.payload_params) == 0


@pytest.mark.parametrize(
    "obs_types",
    [
        ["URL", "MD5", "IP4"],
        [ObservableTypes.URL, ObservableTypes.MD5, ObservableTypes.IP4],
    ],
)
def test_set_observable_types(search_indicator, obs_types):
    expected_result = ["URL", "MD5", "IP4"]
    search_indicator.set_observable_types(obs_types)
    assert len(search_indicator.payload_params) == 1
    assert search_indicator.payload_params.get("types") == expected_result


def test_fail_set_observable_types(search_indicator):
    with pytest.raises(AttributeError):
        search_indicator.set_observable_types(["INVALID", "URL"])
    assert len(search_indicator.payload_params) == 0


@pytest.mark.parametrize(
    "attributes",
    [[{"type": "MALWARE", "value": "ATTRIBUTE"}], [Entity.attribute("MALWARE", "ATTRIBUTE")]],
)
def test_set_attributes(search_indicator, attributes):
    expected_result = [{"type": "MALWARE", "value": "ATTRIBUTE"}]
    search_indicator.set_attributes(attributes)
    assert len(search_indicator.payload_params) == 1
    assert search_indicator.payload_params.get("attributes") == expected_result


@pytest.mark.parametrize(
    "attributes",
    [
        {"type": "INVALID", "value": "ATTRIBUTE"},
        [{"type": "INVALID", "value": "ATTRIBUTE"}],
    ],
)
def test_fail_attributes(search_indicator, attributes):
    with pytest.raises(AttributeError):
        search_indicator.set_attributes(attributes)
    assert len(search_indicator.payload_params) == 0


@pytest.mark.parametrize(
    "observables",
    [[{"type": "URL", "value": "RELATED_OBS"}], [Entity.observable("URL", "RELATED_OBS")]],
)
def test_set_related_observable(search_indicator, observables):
    expected_result = [{"type": "URL", "value": "RELATED_OBS"}]
    search_indicator.set_related_observables(observables)
    assert len(search_indicator.payload_params) == 1
    assert search_indicator.payload_params.get("relatedObservables") == expected_result


@pytest.mark.parametrize(
    "observables",
    [
        {"type": "URL", "value": "RELATED_OBS"},
        [{"type": "INVALID", "value": "RELATED_OBS"}],
    ],
)
def test_set_related_observable_fail(search_indicator, observables):
    with pytest.raises(AttributeError):
        search_indicator.set_related_observables(observables)
    assert len(search_indicator.payload_params) == 0


def test_query_will_not_work_due_to_invalid_dates(search_indicator):
    search_indicator.set_from("1 day ago")
    search_indicator.set_to("2 days ago")
    with pytest.raises(AttributeError):
        search_indicator.search()


def test_ok_query(search_indicator):
    attribute = [{"type": "THREAT_ACTOR", "value": "BAD PANDA"}]
    p = ("cursor", "eyJwYWdlTnVtYmVyIjoxLCJwYWdlU2l6ZSI6Miwib2Zmc2V0Ijo0fQ==")
    q = (
        search_indicator.set_query_term("/Users/mknopf/code/test.sh")
        .set_enclave_ids("3a93fab3-f87a-407a-9376-8eb3fae99b4e")
        .set_priority_scores([3])
        .set_observable_types([ObservableTypes.SOFTWARE.name])
        .set_from(1596607968000)
        .set_to(1598308171000)
        .set_sort_column("PROCESSED_AT")
        .set_attributes(attribute)
        .set_payload_param(*p)
        .search()
    )
    assert q.params.serialize() == json.loads(indicators_example_request)
