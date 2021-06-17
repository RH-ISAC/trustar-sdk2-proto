from __future__ import unicode_literals

import pytest

from trustar2.trustar import TruStar
from trustar2 import TagIndicator, TagSubmission

from tests.conftest import BASE_URL


ENCLAVE_ID = "3a93fab3-f87a-407a-9376-8eb3fae99b4e"
IOC_SUBMISSION_GUID = "cc12a5c6-e575-3879-8e41-2bf240cc6fce"
EXPECTED_URL = BASE_URL.format("/{}/cc12a5c6-e575-3879-8e41-2bf240cc6fce/alter-tags")


@pytest.fixture
def tag_indicator():
    return TagIndicator(
        TruStar(api_key="xxxx", api_secret="xxx", client_metatag="test_env")
    )


@pytest.fixture
def tag_submission():
    return TagSubmission(
        TruStar(api_key="xxxx", api_secret="xxx", client_metatag="test_env")
    )


@pytest.mark.parametrize("added_tags,removed_tags", [(["important", "tag"], []),
                                                     ([], ["not_important", "tag"]),
                                                     (["important", "tag"], ["not_important"])])
def test_ok_alter_tags_indicators(tag_indicator, mocked_request, added_tags, removed_tags):
    
    mocked_request.post(url=EXPECTED_URL.format("indicators"), json={})
    request = (tag_indicator
               .set_added_tags(added_tags)
               .set_removed_tags(removed_tags)
               .set_enclave_id(ENCLAVE_ID)
               .set_indicator_id(IOC_SUBMISSION_GUID)
               )
    request.alter_tags()

    params = request.payload_params.serialize()
    assert params.get("enclaveGuid") == ENCLAVE_ID
    assert params.get("addedTags") == added_tags
    assert params.get("removedTags") == removed_tags


def test_alter_tag_indicators_incomplete_with_missing_indicator_id(tag_indicator):
    with pytest.raises(AttributeError):
        q = (tag_indicator
             .set_added_tags(["tag"])
             .set_enclave_ids(ENCLAVE_ID)
             .alter_tags())


def test_alter_tag_indicators_incomplete_with_missing_enclave_id(tag_indicator):
    # Missing enclave guid
    with pytest.raises(AttributeError):
        q = (tag_indicator
             .set_added_tags(["tag"])
             .set_indicator_id(IOC_SUBMISSION_GUID)
             .alter_tags())


def test_alter_tag_indicators_incomplete_with_missing_tags(tag_indicator):
    with pytest.raises(AttributeError):
        q = (tag_indicator
             .set_enclave_id(ENCLAVE_ID)
             .set_indicator_id(IOC_SUBMISSION_GUID)
             .alter_tags())


@pytest.mark.parametrize("added_tags,removed_tags", [(["important", "tag"], []),
                                                     ([], ["not_important", "tag"]),
                                                     (["important", "tag"], ["not_important"])])
def test_ok_alter_tags_submissions(tag_submission, mocked_request, added_tags, removed_tags):
    
    mocked_request.post(url=EXPECTED_URL.format("submissions"), json={})
    request = (tag_submission
               .set_added_tags(added_tags)
               .set_removed_tags(removed_tags)
               .set_enclave_id(ENCLAVE_ID)
               .set_submission_id(IOC_SUBMISSION_GUID)
               )
    request.alter_tags()

    params = request.payload_params.serialize()
    assert params.get("enclaveId") == ENCLAVE_ID
    assert params.get("addedTags") == added_tags
    assert params.get("removedTags") == removed_tags


def test_alter_tag_submissions_incomplete_with_missing_submission_id(tag_submission):
    with pytest.raises(AttributeError):
        q = (tag_submission
             .set_added_tags(["tag"])
             .set_enclave_id(ENCLAVE_ID)
             .alter_tags())


def test_alter_tag_submissions_incomplete_with_missing_tags(tag_submission):
    # Missing added/removed tags
    with pytest.raises(AttributeError):
        q = (tag_submission
             .set_enclave_id(ENCLAVE_ID)
             .set_submission_id(IOC_SUBMISSION_GUID)
             .alter_tags())


def test_alter_tag_submissions_incomplete_with_missing_enclave_id(tag_submission):
    with pytest.raises(AttributeError):
        q = (tag_submission
             .set_added_tags(["tag"])
             .set_submission_id(IOC_SUBMISSION_GUID)
             .alter_tags())
