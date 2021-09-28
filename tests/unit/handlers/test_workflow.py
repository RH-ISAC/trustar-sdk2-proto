import json
import pytest

from trustar2 import Workflow, TruStar
from trustar2.models import WorkflowConfig
from tests.unit.resources import serialized_workflow_config

URL = "https://api.trustar.co/api/2.0/workflows"
TIMESTAMP = 1583960400000
DEFAULT_PARAMS = 1

@pytest.fixture
def workflow(ts):
    return Workflow(ts)


@pytest.fixture
def workflow_config():
    wf_config = WorkflowConfig()
    wf_config.set_observable_types(["URL", "IP4", "IP6", "SHA256"])
    wf_config.set_priority_scores(["MEDIUM", "HIGH"])
    wf_config.set_source_configs([
        ("test-enclave-id", 3),
        ("test-enclave-id2", 3), 
        ("test-enclave-id3", 1),
        ("test-enclave-id4", 5)
    ])
    wf_config.set_destination_configs(("test-enclave-id", "ENCLAVE"))
    return wf_config


@pytest.fixture
def serialized_wf_config():
    return json.loads(serialized_workflow_config)


@pytest.fixture
def wf_response(serialized_wf_config):
    return {
        "guid": "test-workflow-id",
        "name": "Test Workflow Name",
        "created": TIMESTAMP,
        "updated": TIMESTAMP,
        "workflowConfig": serialized_wf_config
    }


def test_workflow_is_initially_empty(workflow):
    assert len(workflow.payload_params) == 0 + DEFAULT_PARAMS
    assert len(workflow.query_params) == 0


def test_set_type(workflow):
    workflow.set_type("INDICATOR_PRIORITIZATION")
    assert len(workflow.query_params) == 1
    assert workflow.query_params.get("type") == "INDICATOR_PRIORITIZATION"


def test_set_name(workflow):
    workflow.set_name("TEST-WORKFLOW-NAME")
    assert len(workflow.query_params) == 1
    assert len(workflow.payload_params) == 1 + DEFAULT_PARAMS
    assert workflow.query_params.get("name") == "TEST-WORKFLOW-NAME"
    assert workflow.payload_params.get("name") == "TEST-WORKFLOW-NAME" 


def test_set_name_with_string_outside_boundaries(workflow):
    with pytest.raises(AttributeError):
        workflow.set_name("NO")

    with pytest.raises(AttributeError):
        workflow.set_name("N" * 121)


@pytest.mark.parametrize("date", [TIMESTAMP, "2020-03-11T21:00:00"])
def test_set_created_from(workflow, date):
    workflow.set_created_from(date)
    assert len(workflow.query_params) == 1
    assert workflow.query_params.get("createdFrom") == TIMESTAMP


@pytest.mark.parametrize("date", [TIMESTAMP, "2020-03-11T21:00:00"])
def test_set_created_to(workflow, date):
    workflow.set_created_to(date)
    assert len(workflow.query_params) == 1
    assert workflow.query_params.get("createdTo") == TIMESTAMP


@pytest.mark.parametrize("date", [TIMESTAMP, "2020-03-11T21:00:00"])
def test_set_updated_from(workflow, date):
    workflow.set_updated_from(date)
    assert len(workflow.query_params) == 1
    assert workflow.query_params.get("updatedFrom") == TIMESTAMP


@pytest.mark.parametrize("date", [TIMESTAMP, "2020-03-11T21:00:00"])
def test_set_updated_to(workflow, date):
    workflow.set_updated_to(date)
    assert len(workflow.query_params) == 1
    assert workflow.query_params.get("updatedTo") == TIMESTAMP


def test_set_workflow_id(workflow):
    workflow.set_workflow_id("test-workflow-id")
    assert workflow.workflow_guid == "test-workflow-id"


def test_set_safelist_ids(workflow):
    workflow.set_safelist_ids(["test-safelist-id1", "test-safelist-id2"])
    assert len(workflow.payload_params) == 1
    assert workflow.payload_params.get("safelistGuids") == ["test-safelist-id1", "test-safelist-id2"]


def test_set_workflow_config(workflow, workflow_config):
    workflow.set_workflow_config(workflow_config)
    assert len(workflow.payload_params) == 1 + DEFAULT_PARAMS
    assert workflow.payload_params.get("workflowConfig") == json.loads(serialized_workflow_config)


def test_workflow_creation_successful(workflow, mocked_request, workflow_config, wf_response):
    mocked_request.post(URL, json=wf_response)
    workflow.set_name("Test Workflow Name")
    workflow.set_workflow_config(workflow_config)
    workflow.set_safelist_ids([])
    response = workflow.create()
    assert response.status_code == 200
    assert response.data.serialize() == wf_response


def test_workflow_creation_fails_with_missing_payload_field(workflow, workflow_config):
    with pytest.raises(AttributeError):
        workflow.set_workflow_config(workflow_config)
        workflow.set_safelist_ids([])
        response = workflow.create()


def test_workflow_get_by_id(workflow, mocked_request, wf_response):
    mocked_request.get(URL + "/test-workflow-id", json=wf_response)
    workflow.set_workflow_id("test-workflow-id")
    response = workflow.get_by_id()
    assert response.status_code == 200
    assert response.data.serialize() == wf_response


def test_workflow_get_by_id_fails_with_missing_id(workflow, wf_response):
    with pytest.raises(AttributeError):
        response = workflow.get_by_id()


def test_workflow_get_all_workflows(workflow, mocked_request, wf_response):
    mocked_request.get(URL, json={"items": [wf_response]})
    response = workflow.get()
    assert response.status_code == 200
    assert [wf.serialize() for wf in response.data] == [wf_response]


def test_delete_workflow_by_id(workflow, mocked_request):
    mocked_request.delete(URL + "/test-workflow-id", status_code=200)
    workflow.set_workflow_id("test-workflow-id")
    response = workflow.delete()
    assert response.status_code == 200


def test_workflow_delete_fails_with_missing_id(workflow, wf_response):
    with pytest.raises(AttributeError):
        response = workflow.delete()


def test_workflow_update_successful(workflow, mocked_request, workflow_config, wf_response):
    mocked_request.put(URL + "/test-workflow-id", json=wf_response)
    workflow.set_name("Test Workflow Name")
    workflow.set_workflow_config(workflow_config)
    workflow.set_safelist_ids([])
    workflow.set_workflow_id("test-workflow-id")
    response = workflow.update()
    assert response.status_code == 200
    assert response.data.serialize() == wf_response


def test_workflow_update_fails_with_missing_id(workflow, workflow_config):
    with pytest.raises(AttributeError):
        workflow.set_name("Test Workflow Name")
        workflow.set_workflow_config(workflow_config)
        workflow.set_safelist_ids([])
        response = workflow.update()
