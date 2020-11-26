import pytest

from trustar.submission import Submission
from trustar.models import Indicator, Observable, Attribute, Relation


@pytest.fixture
def submission():
    return Submission(None)


@pytest.fixture
def indicators():
    return [
        Indicator(Observable("1.2.3.4", "IP4"), mal_score="HIGH")
        .set_attributes(Relation(Attribute("BAD_PANDA", "MALWARE")))
        .set_related_observables(
            Relation(Observable("bob@gmail.com", "EMAIL_ADDRESS"))
        ),
        Indicator(Observable("5.6.7.8", "IP4"), mal_score="HIGH")
        .set_attributes(Relation(Attribute("BAD_PANDA", "MALWARE")))
        .set_related_observables(Relation(Observable("badurl.com", "URL")))
        .set_tags(["TAG1"]),
    ]


def test_submission_is_empty(submission):
    assert len(submission.params) == 0


def test_set_id(submission):
    submission.set_id("TEST_ID")
    params = [p.value for p in submission.params]
    assert len(submission.params) == 1
    assert params[0] == "TEST_ID"


def test_set_title(submission):
    submission.set_title("TEST_TITLE")
    params = [p.value for p in submission.params]
    assert len(submission.params) == 1
    assert params[0] == "TEST_TITLE"


def test_set_enclave_id(submission):
    submission.set_enclave_id("TEST-ENCLAVE-ID")
    params = [p.value for p in submission.params]
    assert len(submission.params) == 1
    assert params[0] == "TEST-ENCLAVE-ID"


def test_set_external_id(submission):
    submission.set_external_id("TEST-EXTERNAL-ID")
    params = [p.value for p in submission.params]
    assert len(submission.params) == 1
    assert params[0] == "TEST-EXTERNAL-ID"


def test_set_external_url(submission):
    submission.set_external_url("TEST-EXTERNAL-URL")
    params = [p.value for p in submission.params]
    assert len(submission.params) == 1
    assert params[0] == "TEST-EXTERNAL-URL"


def test_set_tags(submission):
    submission.set_tags(["TEST_TAG1", "TEST_TAG2"])
    params = [p.value for p in submission.params]
    assert len(submission.params) == 1
    assert params[0] == ["TEST_TAG1", "TEST_TAG2"]


def test_set_include_content(submission):
    submission.set_include_content(True)
    params = [p.value for p in submission.params]
    assert len(submission.params) == 1
    assert params[0] == True


def test_set_content_indicators(submission, indicators):
    submission.set_content_indicators(indicators)
    serialized_indicators = [i.serialize() for i in indicators]
    params = [p.value for p in submission.params]
    assert params[0]["indicators"] == serialized_indicators


def test_set_raw_content(submission):
    submission.set_raw_content("RAW CONTENT")
    params = [p.value for p in submission.params]
    assert params[0] == "RAW CONTENT"


@pytest.mark.xfail(raises=AttributeError)  # title missing
def test_create_fails_without_mandatory_fields(submission, indicators):
    submission.set_enclave_id("TEST-ENCLAVE_ID")
    submission.set_content_indicators(indicators)
    submission.create()