import json
import pytest

from tests.unit.resources import serialized_workflow_config
from trustar2.models import WorkflowConfig, WorkflowSourceConfig, WorkflowDestinationConfig


TEST_ENCLAVE = "test-enclave-id"


@pytest.fixture
def wf_src_config():
    return WorkflowSourceConfig(TEST_ENCLAVE, 3)


@pytest.fixture
def wf_dst_config():
    return WorkflowDestinationConfig(TEST_ENCLAVE, "ENCLAVE")


@pytest.fixture
def wf_config():
    return WorkflowConfig()


@pytest.fixture
def serialized_wf_config():
    return json.loads(serialized_workflow_config)


def test_workflow_source_config_serialization(wf_src_config):
    serialized = wf_src_config.serialize()
    assert serialized == {"enclaveGuid": TEST_ENCLAVE, "weight": 3}


def test_workflow_destination_config_serialization(wf_dst_config):
    serialized = wf_dst_config.serialize()
    assert serialized == {"enclaveGuid": TEST_ENCLAVE, "destinationType": "ENCLAVE"}


def test_workflow_source_serialization_with_invalid_weight():
    with pytest.raises(AttributeError):
        WorkflowSourceConfig(TEST_ENCLAVE, 6)


def test_workflow_destination_serialization_with_invalid_type():
    with pytest.raises(AttributeError):
        WorkflowDestinationConfig(TEST_ENCLAVE, "INVALID-TYPE")


def test_configs_with_invalid_enclave_id():
    with pytest.raises(AttributeError):
        WorkflowSourceConfig(123456789, 5) # enclave_guid not a string

    with pytest.raises(AttributeError):
        WorkflowDestinationConfig(123456789, "ENCLAVE") # enclave_guid not a string


def test_workflow_config_serialization(wf_config, wf_src_config, wf_dst_config, serialized_wf_config):
    wf_config.set_observable_types(["URL", "IP4", "IP6", "SHA256"])
    wf_config.set_priority_scores(["MEDIUM", "HIGH"])
    wf_config.set_source_configs(wf_src_config) # Using obj
    wf_config.set_source_configs([("test-enclave-id2", 3), ("test-enclave-id3", 1)]) # Using list of tuples
    wf_config.set_source_configs([{"enclave_guid": "test-enclave-id4", "weight": 5}]) # Using dict
    wf_config.set_destination_configs(wf_dst_config)
    assert wf_config.serialize() == serialized_wf_config


def test_workflow_config_set_invalid_obs_types(wf_config):
    with pytest.raises(AttributeError):
        wf_config.set_observable_types(["INVALID_TYPE"])

    with pytest.raises(AttributeError):
        wf_config.set_observable_types("URL") # has to be a list


def test_workflow_config_set_invalid_src_and_dst_config_types(wf_config):
    with pytest.raises(AttributeError):
        wf_config.set_source_configs("STRING-IS-NOT-VALID")

    with pytest.raises(AttributeError):
        wf_config.set_destination_configs(1234567890) # int is not valid


def test_workflow_config_with_missing_properties_in_src_config(wf_config):
    with pytest.raises(AttributeError):
        wf_config.set_source_configs({"enclaveGuid": TEST_ENCLAVE}) # missing weight

    with pytest.raises(AttributeError):
        wf_config.set_source_configs({"weight": 3}) # missing enclave_guid


def test_workflow_config_with_missing_properties_in_dst_config(wf_config):
    with pytest.raises(AttributeError):
        wf_config.set_destination_configs({"enclaveGuid": TEST_ENCLAVE}) # missing destination_type

    with pytest.raises(AttributeError):
        wf_config.set_destination_configs({"destination_type": "QRADAR"}) # missing enclave_guid


def test_wf_config_repr(wf_config):
    assert wf_config.__repr__() == "WorkflowConfig(type=INDICATOR_PRIORITIZATION)"


def test_wf_src_config_repr(wf_src_config):
    assert wf_src_config.__repr__() == "WorkflowSourceConfig(enclave=test-enclave-id, weight=3)"


def test_wf_dst_config_repr(wf_dst_config):
    assert wf_dst_config.__repr__() == "WorkflowDestinationConfig(enclave=test-enclave-id, destination_type=ENCLAVE)"
