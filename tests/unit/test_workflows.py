import json
import pytest

from trustar2 import Workflows, TruStar
from trustar2.models import WorkflowConfig
from tests.unit.resources import serialized_workflow_config

URL = "https://api.trustar.co/api/2.0/workflows"
TIMESTAMP = 1583960400000


@pytest.fixture
def workflows():
    return Workflows(
        TruStar(api_key="xxxx", api_secret="xxx", client_metatag="test_env")
    )


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


def test_workflows_is_initially_empty(workflows):
    assert len(workflows.payload_params) == 0
    assert len(workflows.query_params) == 0


def test_set_type(workflows):
    workflows.set_type("INDICATOR_PRIORITIZATION")
    assert len(workflows.query_params) == 1
    assert workflows.query_params.get("type") == "INDICATOR_PRIORITIZATION"


def test_set_name(workflows):
    workflows.set_name("TEST-WORKFLOW-NAME")
    assert len(workflows.query_params) == 1
    assert len(workflows.payload_params) == 1
    assert workflows.query_params.get("name") == "TEST-WORKFLOW-NAME"
    assert workflows.payload_params.get("name") == "TEST-WORKFLOW-NAME" 


def test_set_name_with_string_outside_boundaries(workflows):
    with pytest.raises(AttributeError):
        workflows.set_name("NO")

    with pytest.raises(AttributeError):
        workflows.set_name("N" * 121)


@pytest.mark.parametrize("date", [TIMESTAMP, "2020-03-11T21:00:00"])
def test_set_created_from(workflows, date):
    workflows.set_created_from(date)
    assert len(workflows.query_params) == 1
    assert workflows.query_params.get("createdFrom") == TIMESTAMP


@pytest.mark.parametrize("date", [TIMESTAMP, "2020-03-11T21:00:00"])
def test_set_created_to(workflows, date):
    workflows.set_created_to(date)
    assert len(workflows.query_params) == 1
    assert workflows.query_params.get("createdTo") == TIMESTAMP


@pytest.mark.parametrize("date", [TIMESTAMP, "2020-03-11T21:00:00"])
def test_set_updated_from(workflows, date):
    workflows.set_updated_from(date)
    assert len(workflows.query_params) == 1
    assert workflows.query_params.get("updatedFrom") == TIMESTAMP


@pytest.mark.parametrize("date", [TIMESTAMP, "2020-03-11T21:00:00"])
def test_set_updated_to(workflows, date):
    workflows.set_updated_to(date)
    assert len(workflows.query_params) == 1
    assert workflows.query_params.get("updatedTo") == TIMESTAMP


def test_set_workflow_id(workflows):
    workflows.set_workflow_id("test-workflow-id")
    assert workflows.workflow_guid == "test-workflow-id"


def test_set_safelist_ids(workflows):
    workflows.set_safelist_ids(["test-safelist-id1", "test-safelist-id2"])
    assert len(workflows.payload_params) == 1
    assert workflows.payload_params.get("safelistGuids") == ["test-safelist-id1", "test-safelist-id2"]


def test_set_workflow_config(workflows, workflow_config):
    workflows.set_workflow_config(workflow_config)
    assert len(workflows.payload_params) == 1
    assert workflows.payload_params.get("workflowConfig") == json.loads(serialized_workflow_config)


def test_workflow_creation_successful(workflows, mocked_request, workflow_config, wf_response):
    mocked_request.post(URL, json=wf_response)
    workflows.set_name("Test Workflow Name")
    workflows.set_workflow_config(workflow_config)
    workflows.set_safelist_ids([])
    response = workflows.create()
    assert response.status_code == 200
    assert response.json() == wf_response


def test_workflows_creation_fails_with_missing_payload_field(workflows, workflow_config):
    with pytest.raises(AttributeError):
        workflows.set_workflow_config(workflow_config)
        workflows.set_safelist_ids([])
        response = workflows.create()


def test_workflow_get_by_id(workflows, mocked_request, wf_response):
    mocked_request.get(URL + "/test-workflow-id", json=wf_response)
    workflows.set_workflow_id("test-workflow-id")
    response = workflows.get_by_id()
    assert response.status_code == 200
    assert response.json() == wf_response


def test_workflow_get_by_id_fails_with_missing_id(workflows, wf_response):
    with pytest.raises(AttributeError):
        response = workflows.get_by_id()


def test_workflow_get_all_workflows(workflows, mocked_request, wf_response):
    mocked_request.get(URL, json=[wf_response])
    response = workflows.get()
    assert response.status_code == 200
    assert response.json() == [wf_response]


def test_delete_workflow_by_id(workflows, mocked_request):
    mocked_request.delete(URL + "/test-workflow-id", status_code=200)
    workflows.set_workflow_id("test-workflow-id")
    response = workflows.delete()
    assert response.status_code == 200


def test_workflow_delete_fails_with_missing_id(workflows, wf_response):
    with pytest.raises(AttributeError):
        response = workflows.delete()


def test_workflow_update_successful(workflows, mocked_request, workflow_config, wf_response):
    mocked_request.put(URL + "/test-workflow-id", json=wf_response)
    workflows.set_name("Test Workflow Name")
    workflows.set_workflow_config(workflow_config)
    workflows.set_safelist_ids([])
    workflows.set_workflow_id("test-workflow-id")
    response = workflows.update()
    assert response.status_code == 200
    assert response.json() == wf_response


def test_workflow_update_fails_with_missing_id(workflows, workflow_config):
    with pytest.raises(AttributeError):
        workflows.set_name("Test Workflow Name")
        workflows.set_workflow_config(workflow_config)
        workflows.set_safelist_ids([])
        response = workflows.update()
