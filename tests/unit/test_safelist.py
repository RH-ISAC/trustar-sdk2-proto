from __future__ import unicode_literals

import json
import pytest

from trustar2 import Safelist, TruStar
from .resources import safelist_summaries, safelist_details, entities_extraction

TRUSTAR_API = "https://test.trustar.co/api/2.0"
SAFELIST_SUMMARIES = TRUSTAR_API + "/safelist-libraries"
SAFELIST_LIBRARY = "test-library-guid-1"
SAFELIST_DETAILS = SAFELIST_SUMMARIES + "/" + SAFELIST_LIBRARY


@pytest.fixture
def safelist():
    config = TruStar(api_key="xxxx", 
                     api_secret="xxx", 
                     client_metatag="test_env", 
                     api_endpoint=TRUSTAR_API)
    return Safelist(config)


@pytest.fixture
def safelist_summaries_json():
    result = json.loads(safelist_summaries)
    return result


@pytest.fixture
def safelist_details_json():
    result = json.loads(safelist_details)
    return result


@pytest.fixture
def entities_extraction_json():
    result = json.loads(entities_extraction)
    return result


def test_get_safelist_summaries(mocked_request, safelist, safelist_summaries_json):
    mocked_request.get(SAFELIST_SUMMARIES, status_code=200, json=safelist_summaries_json)
    response = safelist.get_safelist_libraries()
    assert response.json() == safelist_summaries_json


def test_get_safelist_details_successfully(mocked_request, safelist, safelist_details_json):
    mocked_request.get(SAFELIST_DETAILS, status_code=200, json=safelist_details_json)
    response = safelist.set_library_guid(SAFELIST_LIBRARY).get_safelist_details()
    assert response.json() == safelist_details_json


def test_get_safelist_details_without_library_guid(safelist):
    with pytest.raises(AttributeError):
        safelist.get_safelist_details()


def test_create_entries_successfully(mocked_request, safelist, safelist_details_json):
    mocked_request.patch(SAFELIST_DETAILS, status_code=200, json=safelist_details_json)
    response = safelist \
                .set_library_guid(SAFELIST_LIBRARY) \
                .set_safelist_entries({
                    "entity": "good-email@test-domain.com", 
                    "type": "EMAIL_ADDRESS"
                }).create_entries()

    assert response.json() == safelist_details_json


def test_create_entries_without_library_guid(safelist):
    with pytest.raises(AttributeError):
        safelist.create_entries()


def test_create_entries_without_setting_entries(safelist):
    with pytest.raises(AttributeError):
        safelist.set_library_guid(SAFELIST_LIBRARY).create_entries()


def test_create_entries_without_all_required_fields(safelist):
    with pytest.raises(AttributeError):
        safelist.set_library_guid(SAFELIST_LIBRARY) \
                .set_safelist_entries({
                    "entity": "good-email@test-domain.com"
                }).create_entries()


def test_create_entries_without_strings(safelist):
    with pytest.raises(AttributeError):
        safelist.set_library_guid(SAFELIST_LIBRARY) \
                .set_safelist_entries({
                    100: "good-email@test-domain.com",
                    "type": "EMAIL_ADDRESS"
                }).create_entries()


def test_create_entries_without_valid_type(safelist):
    with pytest.raises(AttributeError):
        safelist.set_library_guid(SAFELIST_LIBRARY) \
                .set_safelist_entries({
                    "entity": "good-email@test-domain.com",
                    "type": "NOT_A_VALID_TYPE"
                }).create_entries()


def test_create_safelist_library_successfully(mocked_request, safelist, safelist_summaries_json):
    mocked_request.post(SAFELIST_SUMMARIES, status_code=200, json=safelist_summaries_json)
    response = safelist.set_library_name("test-library-name-1").create_safelist()
    assert response.json() == safelist_summaries_json


def test_create_safelist_library_without_name(safelist):
    with pytest.raises(AttributeError):
        safelist.create_safelist()


def test_delete_entry_successfully(mocked_request, safelist):
    entry_to_be_deleted = "entry-guid-1"
    url = SAFELIST_DETAILS + "/" + entry_to_be_deleted
    mocked_request.delete(url, status_code=200)
    response = safelist.set_library_guid(SAFELIST_LIBRARY).delete_entry(entry_to_be_deleted)
    assert response.status_code == 200


def test_delete_entry_without_library_guid(safelist):
    with pytest.raises(AttributeError):
        safelist.delete_entry("entry-guid-1")


def test_delete_safelist_library_successfully(mocked_request, safelist):
    mocked_request.delete(SAFELIST_DETAILS, status_code=200)
    response = safelist.set_library_guid(SAFELIST_LIBRARY).delete_safelist()
    assert response.status_code == 200


def test_delete_safelist_library_without_guid(safelist):
    with pytest.raises(AttributeError):
        safelist.delete_safelist()


def test_extract_terms_successfully(mocked_request, safelist, entities_extraction_json):
    url = safelist.extract_endpoint
    mocked_request.post(url, json=entities_extraction_json)
    text_blob = "IP: 8.8.8.8\nUnstructured text extraction\ngood-email@test-domain.com"
    response = safelist.set_text_to_be_extracted(text_blob).extract_terms()
    assert response.json() == entities_extraction_json


def test_extract_terms_without_setting_text(safelist):
    with pytest.raises(AttributeError):
        safelist.extract_terms()
