import json

import pytest

from .resources import enclave
from trustar2.models.enclave import Enclave


NAME = "TestEnclave"
TEMPLATE_NAME = "Private Enclave"
WORKFLOW_SUPPORTED = False
READ = True
CREATE = True
UPDATE = True
ID = "test-id"
TYPE = "INTERNAL"


@pytest.fixture
def enclave_json():
    return json.loads(enclave)


@pytest.fixture
def enclave_obj():
    return Enclave(
        name=NAME, 
        template_name=TEMPLATE_NAME,
        workflow_supported=WORKFLOW_SUPPORTED,
        read=READ,
        create=CREATE,
        update=UPDATE,
        id=ID,
        type=TYPE
    )


def test_enclave_deserialization(enclave_json):
    enclave = Enclave.from_dict(enclave_json)

    assert enclave.name == NAME
    assert enclave.template_name == TEMPLATE_NAME
    assert enclave.workflow_supported == WORKFLOW_SUPPORTED
    assert enclave.read == READ
    assert enclave.create == CREATE
    assert enclave.update == UPDATE
    assert enclave.id == ID
    assert enclave.type == TYPE


def test_enclave_serialization(enclave_obj, enclave_json):
    assert enclave_obj.serialize() == enclave_json


def test_enclave_repr(enclave_obj):
    assert enclave_obj.__repr__() == "Enclave(name={}, id={})".format(NAME, ID)
