import json

import pytest

from tests.unit.resources import safelist_details
from trustar2.models.safelists import SafelistLibrary, SafelistEntry
from trustar2.trustar_enums import ObservableTypes


GUID = "test-library-guid-1"
NAME = "test-library-name-1"
COMPANY_GUID = "test-company-guid-1"
EXCERPT = ""
CREATED_AT = 1618258235178
UPDATED_AT = 1618258235331
CREATED_BY = "test-user-1@trustar.co"
UPDATED_BY = "test-user-1@trustar.co"

ENTRY_GUID = "entry-guid-1"
ENTRY_ENTITY = "good-email@test-domain.com"
ENTRY_TYPE = ObservableTypes.EMAIL_ADDRESS.value
ENTRY_CREATED_BY = "test-user-1@trustar.co"
ENTRY_CREATED_AT = 1618288545871


@pytest.fixture
def safelist_library_with_entries_json():
    return json.loads(safelist_details)


@pytest.fixture
def safelist_library_without_entries_json():
    safelist_dict = json.loads(safelist_details)
    del safelist_dict["entries"]
    return safelist_dict


@pytest.fixture
def safelist_library_without_entries_obj():
    return SafelistLibrary(
        guid=GUID,
        name=NAME,
        created_at=CREATED_AT,
        updated_at=UPDATED_AT,
        created_by=CREATED_BY,
        updated_by=UPDATED_BY,
        company_guid=COMPANY_GUID,
        excerpt=EXCERPT,
        entries=None
    )


@pytest.fixture
def safelist_entry_obj():
    return SafelistEntry(
        guid=ENTRY_GUID,
        entity=ENTRY_ENTITY,
        created_at=ENTRY_CREATED_AT,
        created_by=ENTRY_CREATED_BY,
        type=ENTRY_TYPE
    )


@pytest.fixture
def safelist_library_with_entries_obj(safelist_entry_obj):
    return SafelistLibrary(
        guid=GUID,
        name=NAME,
        created_at=CREATED_AT,
        updated_at=UPDATED_AT,
        created_by=CREATED_BY,
        updated_by=UPDATED_BY,
        company_guid=COMPANY_GUID,
        excerpt=EXCERPT,
        entries=[safelist_entry_obj]
    )


def test_safelist_without_entries_library_deserialization(safelist_library_without_entries_json):
    safelist_library = SafelistLibrary.from_dict(safelist_library_without_entries_json)

    assert safelist_library.guid == GUID
    assert safelist_library.name == NAME
    assert safelist_library.created_at == CREATED_AT
    assert safelist_library.updated_at == UPDATED_AT
    assert safelist_library.created_by == CREATED_BY
    assert safelist_library.updated_by == UPDATED_BY
    assert safelist_library.excerpt == EXCERPT
    assert safelist_library.company_guid == COMPANY_GUID


def test_safelist_library_without_entries_serialization(safelist_library_without_entries_obj, 
                                                        safelist_library_without_entries_json):

    assert safelist_library_without_entries_obj.serialize() == safelist_library_without_entries_json


def test_safelist_library_repr(safelist_library_without_entries_obj):
    assert safelist_library_without_entries_obj.__repr__() == "SafelistLibrary(name={}, guid={})".format(NAME, GUID)


def test_safelist_with_entries_library_deserialization(safelist_library_with_entries_json):
    safelist_library = SafelistLibrary.from_dict(safelist_library_with_entries_json)

    assert safelist_library.guid == GUID
    assert safelist_library.name == NAME
    assert safelist_library.created_at == CREATED_AT
    assert safelist_library.updated_at == UPDATED_AT
    assert safelist_library.created_by == CREATED_BY
    assert safelist_library.updated_by == UPDATED_BY
    assert safelist_library.excerpt == EXCERPT
    assert safelist_library.company_guid == COMPANY_GUID

    assert safelist_library.entries[0].guid == ENTRY_GUID
    assert safelist_library.entries[0].entity == ENTRY_ENTITY
    assert safelist_library.entries[0].type == ENTRY_TYPE
    assert safelist_library.entries[0].created_by == ENTRY_CREATED_BY
    assert safelist_library.entries[0].created_at == ENTRY_CREATED_AT


def test_safelist_entry_repr(safelist_entry_obj):
    assert safelist_entry_obj.__repr__() == "SafelistEntry(entity={}, type={})".format(ENTRY_ENTITY, ENTRY_TYPE)
