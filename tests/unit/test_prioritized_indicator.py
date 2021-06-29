import json
import pytest
from .resources import prioritized_indicator
from trustar2.models.prioritized_indicator import PrioritizedIndicator


@pytest.fixture
def prioritized_indicator_json():
    return json.loads(prioritized_indicator)


def test_prioritized_indicator_deserialization(prioritized_indicator_json):
    prioritized_ioc = PrioritizedIndicator.from_dict(prioritized_indicator_json)

    assert prioritized_ioc.guid == "test-guid"
    assert prioritized_ioc.enclave_guid == "test-enclave-guid"
    assert prioritized_ioc.workflow_guid == "test-workflow-guid"
    assert prioritized_ioc.observable.value == "2.2.2.2"
    assert prioritized_ioc.observable.type == "IP4"
    assert prioritized_ioc.priority_score == "HIGH"
    assert prioritized_ioc.attributes[0].value == "MalwareName"
    assert prioritized_ioc.attributes[0].type == "MALWARE"
    assert prioritized_ioc.user_tags == []
    assert prioritized_ioc.submission_tags == ["malware"]
    # assert prioritized_ioc.score_contexts = score_contexts
    assert prioritized_ioc.created == 1616176082000
    assert prioritized_ioc.updated == 1624986245000
    assert prioritized_ioc.processed_at == 1624990135728
    assert not prioritized_ioc.safelisted
