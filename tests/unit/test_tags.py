from __future__ import unicode_literals
from trustar2.handlers.tags import TagObservable

import pytest

from trustar2.trustar import TruStar
from trustar2 import TagIndicator, TagSubmission

from tests.conftest import BASE_URL

ENCLAVE_ID = "3a93fab3-f87a-407a-9376-8eb3fae99b4e"
IOC_SUBMISSION_GUID = "cc12a5c6-e575-3879-8e41-2bf240cc6fce"
OBSERVABLE_VALUE = "b1fa0ef4930abc0c681081ef2d2f834b3b2fbbbd"
EXPECTED_URL = BASE_URL.format("/{}/cc12a5c6-e575-3879-8e41-2bf240cc6fce/alter-tags")

@pytest.fixture
def tag_indicator(ts):
    return TagIndicator(ts)

@pytest.fixture
def tag_submission(ts):
    return TagSubmission(ts)

@pytest.fixture
def tag_observable(ts):
    return TagObservable(ts)

## Indicator Tags

@pytest.mark.parametrize(
    ("added_tags, removed_tags"),
    (
        (["important", "tag"], []),
        ([], ["not_important", "tag"]),
        (["important", "tag"], ["not_important"])
    )
)
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

## Submissions Tags

@pytest.mark.parametrize(
    ("added_tags, removed_tags"),
    (
        (["important", "tag"], []),
        ([], ["not_important", "tag"]),
        (["important", "tag"], ["not_important"])
    )
)
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


## Observable Tags

@pytest.mark.parametrize(
    ("added_tags, removed_tags"),
    (
        (["important", "tag"], []),
        ([], ["not_important", "tag"]),
        (["important", "tag"], ["not_important"])
    )
)
def test_ok_alter_tags_observables(tag_observable, mocked_request, added_tags, removed_tags):

    EXPECTED_URL = BASE_URL.format("/observables/alter-tags")

    mocked_request.post(url=EXPECTED_URL, json={
        "addedTags": added_tags,
        "removedTags": removed_tags
    })

    request = (tag_observable
               .set_added_tags(added_tags)
               .set_removed_tags(removed_tags)
               .set_enclave_id(ENCLAVE_ID)
               .set_observable_value(OBSERVABLE_VALUE)
               )

    request.alter_tags()

    params = request.payload_params.serialize()
    assert params.get("enclaveGuid") == ENCLAVE_ID
    assert params.get("addedTags") == added_tags
    assert params.get("removedTags") == removed_tags


def test_alter_tag_observables_incomplete_with_missing_observable_value(tag_observable):
    with pytest.raises(AttributeError):
        q = (tag_observable
                .set_added_tags(["tag"])
                .set_enclave_id(ENCLAVE_ID)
                .alter_tags())


def test_alter_tag_observables_incomplete_with_missing_enclave_id(tag_observable):
    with pytest.raises(AttributeError):
        q = (tag_observable
             .set_added_tags(["tag"])
             .set_observable_value(OBSERVABLE_VALUE)
             .alter_tags())


def test_alter_tag_observables_incomplete_with_missing_tags(tag_observable):
    with pytest.raises(AttributeError):
        q = (tag_observable
             .set_enclave_id(ENCLAVE_ID)
             .set_observable_value(IOC_SUBMISSION_GUID)
             .alter_tags())

def test_alter_tag_observables_incomplete_with_empty_tags(tag_observable):
    with pytest.raises(AttributeError):
        q = (tag_observable
                .set_enclave_id(ENCLAVE_ID)
                .set_observable_value(IOC_SUBMISSION_GUID)
                .set_added_tags([])
                .set_removed_tags([])
                .alter_tags())
