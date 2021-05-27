from __future__ import unicode_literals

import json
import pytest

from trustar2 import Submission, TruStar
from trustar2.models import Indicator, Entity

from tests.unit.resources import submission_example_request


@pytest.fixture
def submission():
    return Submission(
        TruStar(api_key="xxxx", api_secret="xxx", client_metatag="test_env")
    )


TOTAL_DEFAULT_PARAMS = 1

@pytest.fixture
def indicators():
    bad_panda = Entity.attribute("MALWARE", "BAD_PANDA")
    related_observable_email = Entity.observable("EMAIL_ADDRESS", "bob@gmail.com")
    related_observable_bad_url = Entity.observable("URL", "badurl.com")
    return [
        Indicator("IP4", "1.2.3.4")
        .set_malicious_score("HIGH")
        .set_attributes(bad_panda)
        .set_related_observables(related_observable_email),
        Indicator("IP4", "5.6.7.8")
        .set_malicious_score("HIGH")
        .set_attributes(bad_panda)
        .set_related_observables(related_observable_bad_url)
        .set_tags(["TAG1"]),
    ]


def test_submission_is_empty(submission):
    assert len(submission.payload_params) == TOTAL_DEFAULT_PARAMS


def test_set_id(submission):
    submission.set_id("TEST_ID")
    params = [p.value for p in submission.payload_params]
    assert len(submission.payload_params) == TOTAL_DEFAULT_PARAMS + 1
    assert "TEST_ID" in params


def test_set_title(submission):
    submission.set_title("TEST_TITLE")
    params = [p.value for p in submission.payload_params]
    assert len(submission.payload_params) == TOTAL_DEFAULT_PARAMS + 1
    assert "TEST_TITLE" in params


def test_set_enclave_id(submission):
    submission.set_enclave_id("TEST-ENCLAVE-ID")
    params = [p.value for p in submission.payload_params]
    assert len(submission.payload_params) == TOTAL_DEFAULT_PARAMS + 1
    assert  "TEST-ENCLAVE-ID" in params


def test_set_external_id(submission):
    submission.set_external_id("TEST-EXTERNAL-ID")
    params = [p.value for p in submission.payload_params]
    assert len(submission.payload_params) == TOTAL_DEFAULT_PARAMS + 1
    assert "TEST-EXTERNAL-ID" in params


def test_set_external_url(submission):
    submission.set_external_url("TEST-EXTERNAL-URL")
    params = [p.value for p in submission.payload_params]
    assert len(submission.payload_params) == TOTAL_DEFAULT_PARAMS + 1
    assert "TEST-EXTERNAL-URL" in params


def test_set_tags(submission):
    submission.set_tags(["TEST_TAG1", "TEST_TAG2"])
    params = [p.value for p in submission.payload_params]
    assert len(submission.payload_params) == TOTAL_DEFAULT_PARAMS
    assert ["TEST_TAG1", "TEST_TAG2"] in params


def test_set_include_content(submission):
    submission.set_include_content(True)
    params = [p.value for p in submission.query_params]
    assert len(submission.query_params) == 1
    assert True in params


def test_set_content_indicators(submission, indicators):
    submission.set_content_indicators(indicators)
    serialized_indicators = [i.serialize() for i in indicators]
    # hacky workaround for python2 unsorted dicts
    params = [p.value for p in submission.payload_params if p.value != []]
    assert serialized_indicators == params[0]["indicators"]


def test_set_raw_content(submission):
    submission.set_raw_content("RAW CONTENT")
    params = [p.value for p in submission.payload_params]
    assert "RAW CONTENT" in params


@pytest.mark.parametrize("date", [1583960400000, "2020-03-11T21:00:00"])
def test_set_timestamp(submission, date):
    submission.set_timestamp(date)
    assert submission.payload_params.get("timestamp") == 1583960400000
    assert len(submission.payload_params) == TOTAL_DEFAULT_PARAMS + 1


def test_create_fails_without_mandatory_fields(submission, indicators):
    submission.set_enclave_id("TEST-ENCLAVE_ID")
    submission.set_content_indicators(indicators)
    with pytest.raises(AttributeError):
        submission.create()


@pytest.fixture
def complex_indicator():
    threat_actor = (
        Entity.attribute("THREAT_ACTOR", "ActorName")
        .set_valid_from(1604510497000)
        .set_valid_to(1607102497000)
        .set_confidence_score("LOW")
    )

    malware = (
        Entity.attribute("MALWARE", "MalwareName")
        .set_valid_from(1604510497000)
        .set_valid_to(1607102497000)
        .set_confidence_score("MEDIUM")
    )
    ip4 = (
        Entity.observable("IP4", "2.2.2.2")
        .set_valid_from(1604510497000)
        .set_valid_to(1607102497000)
        .set_confidence_score("LOW")
    )
    url = (
        Entity.observable("URL", "wwww.relatedUrl.com")
        .set_valid_from(1604510497000)
        .set_valid_to(1607102497000)
        .set_confidence_score("HIGH")
    )
    indicator = [
        Indicator("URL", "verybadurl")
        .set_valid_from(1604510497000)
        .set_valid_to(1607102497000)
        .set_confidence_score("LOW")
        .set_malicious_score("BENIGN")
        .set_attributes([threat_actor, malware])
        .set_related_observables([ip4, url])
        .set_properties({"propertyKey": "propertyValue"})
        .set_tags(["importantTag", "anotherTag"])
    ]
    return indicator


@pytest.fixture
def full_submission(submission, complex_indicator):
    return (
        submission.set_title("Report, complex test")
        .set_content_indicators(complex_indicator)
        .set_enclave_id("c0f07a9f-76e4-48df-a0d4-c63ed2edccf0")
        .set_external_id("external-1234")
        .set_external_url("externalUrlValue")
        .set_timestamp(1607102497000)
        .set_tags(["random_tag"])
        .set_raw_content("blob of text")
    )


def test_submission_ok_json(full_submission):
    assert full_submission.payload_params.serialize() == json.loads(submission_example_request)


def test_ok_submission_ok(mocked_request, full_submission):
    expected_url = "https://api.trustar.co/api/2.0/submissions/indicators/upsert"
    mocked_request.post(url=expected_url, json={"id": "TEST-ID", "submissionVersion": 1})
    response = full_submission.upsert()
    assert response.json().get("submissionVersion") == 1
    mocked_request.post(url=expected_url, json={"id": "TEST-ID", "submissionVersion": 2})
    response = full_submission.upsert()
    assert response.json().get("submissionVersion") == 2
