import json

import pytest

from tests.unit.resources import serialized_workflow
from trustar2.models.workflow import Workflow
from trustar2.models.workflow_configs import WorkflowConfig
from trustar2.trustar_enums import ObservableTypes, MaliciousScore, WorkflowDestinations


GUID = "test-guid"
NAME = "Test Workflow"
CREATED = 1616706603077
UPDATED = 1621540733425
SAFELIST_GUIDS = ["test-safelist-id"]
SOURCE_ENCLAVE_ID = "test-source-id"
WEIGHT = 1
DEST_ENCLAVE_ID = "test-destination-id"
DEST_TYPE = WorkflowDestinations.ENCLAVE.value

TYPES = [ObservableTypes.IP4.value, ObservableTypes.IP6.value, ObservableTypes.EMAIL_ADDRESS.value, 
         ObservableTypes.URL.value, ObservableTypes.MD5.value, ObservableTypes.SHA256.value]

SCORES = [MaliciousScore.MEDIUM.value, MaliciousScore.HIGH.value]



@pytest.fixture
def workflow_json():
    return json.loads(serialized_workflow)


@pytest.fixture
def workflow_obj():
    wf_config = WorkflowConfig()
    wf_config.set_source_configs((SOURCE_ENCLAVE_ID, WEIGHT))
    wf_config.set_destination_configs((DEST_ENCLAVE_ID, DEST_TYPE))
    wf_config.set_priority_scores(SCORES)
    wf_config.set_observable_types(TYPES)
    return Workflow(
        guid=GUID,
        name=NAME,
        created=CREATED,
        updated=UPDATED,
        safelist_guids=SAFELIST_GUIDS,
        workflow_config=wf_config
    )


def test_workflow_deserialization(workflow_json):
    workflow = Workflow.from_dict(workflow_json)

    assert workflow.guid == GUID
    assert workflow.name == NAME
    assert workflow.created == CREATED
    assert workflow.updated == UPDATED
    assert workflow.safelist_guids == SAFELIST_GUIDS
    
    assert workflow.workflow_config.workflow_source[0].enclave_guid == SOURCE_ENCLAVE_ID
    assert workflow.workflow_config.workflow_source[0].weight == WEIGHT

    assert workflow.workflow_config.workflow_destination[0].enclave_guid == DEST_ENCLAVE_ID
    assert workflow.workflow_config.workflow_destination[0].destination_type == DEST_TYPE

    assert workflow.workflow_config.priority_scores == SCORES
    assert workflow.workflow_config.observable_types == TYPES
    

def test_workflow_serialization(workflow_obj, workflow_json):
    assert workflow_obj.serialize() == workflow_json


def test_workflow_repr(workflow_obj):
    assert workflow_obj.__repr__() == "Workflow(name={}, guid={})".format(NAME, GUID)
