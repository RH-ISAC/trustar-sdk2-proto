import json
import pytest
from .resources import searched_submission
from trustar2.models.searched_submission import SearchedSubmission


@pytest.fixture
def searched_submission_json():
    return json.loads(searched_submission)


def test_searched_submission_deserialization(searched_submission_json):
    searched_submission = SearchedSubmission.from_dict(searched_submission_json)

    assert searched_submission.title == "Test Submission Title"
    assert searched_submission.guid == "test-guid"
    assert searched_submission.enclave_guid == "test-enclave-guid"
    assert searched_submission.created == 1624980621003
    assert searched_submission.updated == 1624980621003
    assert searched_submission.tags == []
