import json

import pytest

from tests.unit.resources import prioritized_indicator
from trustar2.models.entity import Entity
from trustar2.models.score_context import ScoreContext
from trustar2.models.prioritized_indicator import PrioritizedIndicator
from trustar2.trustar_enums import ObservableTypes, AttributeTypes, MaliciousScore


IOC_GUID = "test-guid"
ENCLAVE_GUID = "test-enclave-guid"
WORKFLOW_GUID = "test-workflow-guid"
OBS_VALUE = "2.2.2.2"
OBS_TYPE = ObservableTypes.IP4.value
PRIORITY_SCORE = MaliciousScore.HIGH.value
ATTR_VALUE = "MalwareName"
ATTR_TYPE = AttributeTypes.MALWARE.value
USER_TAGS = []
SUBMISSION_TAGS = ["malware"]
CREATED = 1616176082000
UPDATED = 1624986245000
PROCESSED_AT = 1624990135728
SC_ENCLAVE_GUID = "test-score-context-enclave-guid"
SC_SOURCE_NAME = "Test Source"
SC_NORMALIZED_SCORE = 3
SC_WEIGHT = 3.0
SC_PROPERTIES = {}
SC_ENCLAVE_NAME = "Test Source"


@pytest.fixture
def prioritized_indicator_json():
    return json.loads(prioritized_indicator)


@pytest.fixture
def prioritized_indicator_obj():
    return PrioritizedIndicator(
        guid=IOC_GUID,
        enclave_guid=ENCLAVE_GUID,
        workflow_guid=WORKFLOW_GUID,
        observable=Entity.observable(OBS_TYPE, OBS_VALUE),
        priority_score=PRIORITY_SCORE,
        attributes=[Entity.attribute(ATTR_TYPE, ATTR_VALUE)],
        user_tags=USER_TAGS,
        submission_tags=SUBMISSION_TAGS,
        score_contexts=[ScoreContext(
            enclave_guid=SC_ENCLAVE_GUID,
            source_name=SC_SOURCE_NAME,
            normalized_score=SC_NORMALIZED_SCORE,
            weight=SC_WEIGHT,
            properties=SC_PROPERTIES,
            enclave_name=SC_ENCLAVE_NAME
        )],
        created=CREATED,
        updated=UPDATED,
        processed_at=PROCESSED_AT,
        safelisted=False
    )


def test_prioritized_indicator_deserialization(prioritized_indicator_json):
    prioritized_ioc = PrioritizedIndicator.from_dict(prioritized_indicator_json)

    assert prioritized_ioc.guid == IOC_GUID
    assert prioritized_ioc.enclave_guid == ENCLAVE_GUID
    assert prioritized_ioc.workflow_guid == WORKFLOW_GUID
    assert prioritized_ioc.observable.value == OBS_VALUE
    assert prioritized_ioc.observable.type == OBS_TYPE
    assert prioritized_ioc.priority_score == PRIORITY_SCORE
    assert prioritized_ioc.attributes[0].value == ATTR_VALUE
    assert prioritized_ioc.attributes[0].type == ATTR_TYPE
    assert prioritized_ioc.user_tags == USER_TAGS
    assert prioritized_ioc.submission_tags == SUBMISSION_TAGS
    assert prioritized_ioc.score_contexts[0].enclave_guid == SC_ENCLAVE_GUID
    assert prioritized_ioc.score_contexts[0].source_name == SC_SOURCE_NAME
    assert prioritized_ioc.score_contexts[0].weight == SC_WEIGHT
    assert prioritized_ioc.score_contexts[0].normalized_score == SC_NORMALIZED_SCORE
    assert prioritized_ioc.score_contexts[0].enclave_name == SC_ENCLAVE_NAME
    assert prioritized_ioc.score_contexts[0].properties == SC_PROPERTIES
    assert prioritized_ioc.created == CREATED
    assert prioritized_ioc.updated == UPDATED
    assert prioritized_ioc.processed_at == PROCESSED_AT
    assert not prioritized_ioc.safelisted


def test_prioritized_indicator_serialization(prioritized_indicator_obj, prioritized_indicator_json):
    assert prioritized_indicator_obj.serialize() == prioritized_indicator_json


def test_prioritized_indicator_repr(prioritized_indicator_obj):
    assert prioritized_indicator_obj.__repr__() == "PrioritizedIndicator(type=IP4, value=2.2.2.2)"
