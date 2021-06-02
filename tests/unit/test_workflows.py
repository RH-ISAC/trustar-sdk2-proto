import json
import pytest

from trustar2 import Workflows, TruStar
from trustar2.models import WorkflowConfig
from tests.unit.resources import serialized_workflow_config


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


@pytest.mark.parametrize("date", [1583960400000, "2020-03-11T21:00:00"])
def test_set_created_from(workflows, date):
    workflows.set_created_from(date)
    assert len(workflows.query_params) == 1
    assert workflows.query_params.get("createdFrom") == 1583960400000


@pytest.mark.parametrize("date", [1583960400000, "2020-03-11T21:00:00"])
def test_set_created_to(workflows, date):
    workflows.set_created_to(date)
    assert len(workflows.query_params) == 1
    assert workflows.query_params.get("createdTo") == 1583960400000


@pytest.mark.parametrize("date", [1583960400000, "2020-03-11T21:00:00"])
def test_set_updated_from(workflows, date):
    workflows.set_updated_from(date)
    assert len(workflows.query_params) == 1
    assert workflows.query_params.get("updatedFrom") == 1583960400000


@pytest.mark.parametrize("date", [1583960400000, "2020-03-11T21:00:00"])
def test_set_updated_to(workflows, date):
    workflows.set_updated_to(date)
    assert len(workflows.query_params) == 1
    assert workflows.query_params.get("updatedTo") == 1583960400000


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



# TODO: missing tests mocking and checking the HTTP requests are well formed

