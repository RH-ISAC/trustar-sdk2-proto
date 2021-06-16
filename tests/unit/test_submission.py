from __future__ import unicode_literals

import json
import pytest

from trustar2 import Submission, TruStar
from trustar2.models import Indicator, Entity

from tests.unit.resources import (
    indicators_submission_example_request, 
    non_structured_submission_example_request
)


TOTAL_DEFAULT_PARAMS = 1
BASE_URL = "https://api.trustar.co/api/2.0/submissions{}"
ENCLAVE_ID = "c0f07a9f-76e4-48df-a0d4-c63ed2edccf0"
TIMESTAMP = 1583960400000


@pytest.fixture
def submission():
    return Submission(
        TruStar(api_key="xxxx", api_secret="xxx", client_metatag="test_env")
    )


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


def test_set_query_term(submission):
    submission.set_query_term("TEST_TERM")
    values = [param.value for param in submission.payload_params]
    assert len(submission.payload_params) == TOTAL_DEFAULT_PARAMS + 1
    assert "TEST_TERM" in values


@pytest.mark.parametrize("from_date", [TIMESTAMP, "2020-03-11T21:00:00"])
def test_set_from(submission, from_date):
    submission.set_from(from_date)
    assert submission.payload_params.get("from") == TIMESTAMP
    assert len(submission.payload_params) == TOTAL_DEFAULT_PARAMS + 1


def test_set_from_fail(submission):
    with pytest.raises(TypeError):
        submission.set_from("XXXX-XX-XX")
    assert len(submission.payload_params) == TOTAL_DEFAULT_PARAMS


@pytest.mark.parametrize("to_date", [TIMESTAMP, "2020-03-11T21:00:00+00:00"])
def test_set_to(submission, to_date):
    submission.set_to(to_date)
    assert submission.payload_params.get("to") == TIMESTAMP
    assert len(submission.payload_params) == TOTAL_DEFAULT_PARAMS + 1


def test_set_to_fail(submission):
    with pytest.raises(TypeError):
        submission.set_to("XXXX-XX-XX")
    assert len(submission.payload_params) == TOTAL_DEFAULT_PARAMS


def test_set_sort_column(submission):
    submission.set_sort_column("UPDATED")
    assert len(submission.payload_params) == TOTAL_DEFAULT_PARAMS + 1
    assert submission.payload_params.get("sortColumn") == "UPDATED"


def test_set_sort_column_fail(submission):
    with pytest.raises(AttributeError):
        submission.set_sort_column("INVALID_NAME")
    assert len(submission.payload_params) == TOTAL_DEFAULT_PARAMS


def test_set_included_tags(submission):
    submission.set_included_tags(["test-tag"])
    assert len(submission.payload_params) == TOTAL_DEFAULT_PARAMS + 1
    assert submission.payload_params.get("includedTags") == ["test-tag"]


def test_set_excluded_tags(submission):
    submission.set_excluded_tags(["test-tag"])
    assert len(submission.payload_params) == TOTAL_DEFAULT_PARAMS + 1
    assert submission.payload_params.get("excludedTags") == ["test-tag"]


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


@pytest.mark.parametrize("date", [TIMESTAMP, "2020-03-11T21:00:00"])
def test_set_timestamp(submission, date):
    submission.set_timestamp(date)
    assert submission.payload_params.get("timestamp") == TIMESTAMP
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
def full_submission(submission):
    return (
        submission.set_title("Report, complex test")
        .set_enclave_id(ENCLAVE_ID)
        .set_external_id("external-1234")
        .set_external_url("externalUrlValue")
        .set_timestamp(1607102497000)
        .set_tags(["random_tag"])
    )


@pytest.fixture
def full_iocs_submission(full_submission, complex_indicator):
    return (
        full_submission.set_content_indicators(complex_indicator)
        .set_raw_content("blob of text")
    )


@pytest.fixture
def full_events_submission(full_submission):
    return full_submission.set_content_events("MALICIOUS IP: 8.8.8.8")


@pytest.fixture
def full_intelligence_submission(full_submission):
    return full_submission.set_content_intelligence("MALICIOUS IP: 8.8.8.8")


def test_indicators_submission_ok_json(full_iocs_submission):
    serialized_submission = json.loads(indicators_submission_example_request)
    assert full_iocs_submission.payload_params.serialize() == serialized_submission


def test_non_structured_submission_ok_json(full_events_submission, full_intelligence_submission):
    serialized_subnmission = json.loads(non_structured_submission_example_request)
    assert full_events_submission.payload_params.serialize() == serialized_subnmission
    assert full_intelligence_submission.payload_params.serialize() == serialized_subnmission


def test_indicators_submission_ok(mocked_request, full_iocs_submission):
    expected_url = BASE_URL.format("/indicators/upsert")
    mocked_request.post(url=expected_url, json={"id": "TEST-ID", "submissionVersion": 1})
    response = full_iocs_submission.upsert()
    assert response.json().get("submissionVersion") == 1
    mocked_request.post(url=expected_url, json={"id": "TEST-ID", "submissionVersion": 2})
    response = full_iocs_submission.upsert()
    assert response.json().get("submissionVersion") == 2


def test_events_submission_ok(mocked_request, full_events_submission):
    expected_url = BASE_URL.format("/events/upsert")
    mocked_request.post(url=expected_url, json={"id": "TEST-ID", "submissionVersion": 1})
    response = full_events_submission.upsert()
    assert response.json().get("submissionVersion") == 1
    mocked_request.post(url=expected_url, json={"id": "TEST-ID", "submissionVersion": 2})
    response = full_events_submission.upsert()
    assert response.json().get("submissionVersion") == 2


def test_intelligence_submission_ok(mocked_request, full_intelligence_submission):
    expected_url = BASE_URL.format("/intelligence/upsert")
    mocked_request.post(url=expected_url, json={"id": "TEST-ID", "submissionVersion": 1})
    response = full_intelligence_submission.upsert()
    assert response.json().get("submissionVersion") == 1
    mocked_request.post(url=expected_url, json={"id": "TEST-ID", "submissionVersion": 2})
    response = full_intelligence_submission.upsert()
    assert response.json().get("submissionVersion") == 2


def test_changing_content_will_change_url(full_submission):
    full_submission.set_content_indicators([Indicator("IP4", "8.8.8.8")])
    assert full_submission._submission_category == "/indicators"
    
    full_submission.set_content_events("test-event")
    assert full_submission._submission_category == "/events"
    
    full_submission.set_content_intelligence("test-intelligence")
    assert full_submission._submission_category == "/intelligence"


def test_get_structured_indicators_submissions(submission, mocked_request):
    json_response = json.loads(indicators_submission_example_request)
    endpoint = "/indicators?id=external-1234&idType=EXTERNAL&enclaveGuid={}&includeContent=true".format(ENCLAVE_ID)
    expected_url = BASE_URL.format(endpoint)
    mocked_request.get(expected_url, json=json_response)

    submission.set_enclave_id(ENCLAVE_ID)
    submission.set_external_id("external-1234")
    submission.set_id_type_as_external(True)
    submission.set_include_content(True)

    response = submission.get(structured_indicators=True)
    assert response.json() == json_response


def test_get_non_structured_submissions(submission, mocked_request):
    json_response = json.loads(non_structured_submission_example_request)
    endpoint = "/events?id=external-1234&idType=EXTERNAL&enclaveGuid={}&includeContent=true".format(ENCLAVE_ID)
    expected_url = BASE_URL.format(endpoint)
    mocked_request.get(expected_url, json=json_response)

    submission.set_enclave_id(ENCLAVE_ID)
    submission.set_external_id("external-1234")
    submission.set_id_type_as_external(True)
    submission.set_include_content(True)

    response = submission.get(structured_indicators=False)
    assert response.json() == json_response


def test_get_submission_status(submission, mocked_request):
    json_response = {"id": "d11513f4-0dc9-4aab-b993-e925225d4c68", "status": "SUBMISSION_SUCCESS"}
    expected_url = BASE_URL.format("/test-submission-id/status")
    mocked_request.get(expected_url, json=json_response)
    response = submission.get_submission_status("test-submission-id")
    assert response.json() == json_response
