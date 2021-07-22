from __future__ import unicode_literals

import json

import pytest

from trustar2.models import Indicator, Entity
from tests.unit.resources import indicators_submission_example_request
from trustar2.trustar_enums import (
    ObservableTypes, AttributeTypes, 
    ConfidenceScore, MaliciousScore
)


URL = ObservableTypes.URL.value
IP4 = ObservableTypes.IP4.value
EMAIL_ADDRESS = ObservableTypes.EMAIL_ADDRESS.value
THREAT_ACTOR = AttributeTypes.THREAT_ACTOR.value
MALWARE = AttributeTypes.MALWARE.value

FROM_TIMESTAMP = 1604510497000
TO_TIMESTAMP = 1607102497000

LOW_CONFIDENCE = ConfidenceScore.LOW.value
MEDIUM_CONFIDENCE = ConfidenceScore.MEDIUM.value
HIGH_CONFIDENCE = ConfidenceScore.HIGH.value
BENIGN_SCORE = MaliciousScore.BENIGN.value


@pytest.fixture
def indicator():
    return Indicator(URL, "www.badurl.com")


@pytest.fixture
def indicator_json():
    return json.loads(indicators_submission_example_request).get("content").get("indicators")[0]


def test_set_related_observables(indicator):
    related_observable_email = Entity.observable(EMAIL_ADDRESS, "bob@gmail.com")
    indicator.set_related_observables(related_observable_email)
    assert related_observable_email in indicator.related_observables


def test_set_attributes(indicator):
    attributes = Entity.attribute(THREAT_ACTOR, "ActorName")
    indicator.set_attributes(attributes)
    assert attributes in indicator.attributes


def test_set_valid_to(indicator):
    indicator.set_valid_to(1604510497)
    value = indicator.observable.params.get("validTo")
    assert value == 1604510497


def test_set_valid_from(indicator):
    indicator.set_valid_from(1604510497)
    value = indicator.observable.params.get("validFrom")
    assert value == 1604510497


def test_set_malicious_score(indicator):
    indicator.set_malicious_score("HIGH")
    value = indicator.observable.params.get("maliciousScore")
    assert value == "HIGH"


def test_set_confidence_score(indicator):
    indicator.set_confidence_score("HIGH")
    value = indicator.observable.params.get("confidenceScore")
    assert value == "HIGH"

 
def test_set_properties(indicator):
    properties = {"myPropKey": "myPropValue"}
    indicator.set_properties(properties)
    value = indicator.observable.params.get("properties")
    assert value == properties


def test_set_properties_with_more_than_twenty_elements(indicator):
    properties = {"prop" + str(i): "value" + str(i) for i in range(21)}
    with pytest.raises(AttributeError):
        indicator.set_properties(properties)


def test_set_properties_with_element_type_not_a_string(indicator):
    properties = {"myProperty": 100}
    with pytest.raises(AttributeError):
        indicator.set_properties(properties)


def test_set_tags(indicator):
    tag = ["importantTag"]
    indicator.set_tags(tag)
    assert "importantTag" in indicator.tags


def test_indicator_deserialization(indicator_json):
    indicator = Indicator.from_dict(indicator_json)
    assert indicator.observable.type == URL
    assert indicator.observable.value == "verybadurl"
    assert indicator.confidence_score == LOW_CONFIDENCE
    assert indicator.malicious_score == BENIGN_SCORE
    assert indicator.properties == {"propertyKey": "propertyValue"}
    assert indicator.valid_from == FROM_TIMESTAMP
    assert indicator.valid_to == TO_TIMESTAMP

    assert indicator.attributes[0].type == THREAT_ACTOR
    assert indicator.attributes[0].value == "ActorName"
    assert indicator.attributes[0].valid_from == FROM_TIMESTAMP
    assert indicator.attributes[0].valid_to == TO_TIMESTAMP
    assert indicator.attributes[0].confidence_score == LOW_CONFIDENCE
    
    assert indicator.attributes[1].type == MALWARE
    assert indicator.attributes[1].value == "MalwareName"
    assert indicator.attributes[1].valid_from == FROM_TIMESTAMP
    assert indicator.attributes[1].valid_to == TO_TIMESTAMP
    assert indicator.attributes[1].confidence_score == MEDIUM_CONFIDENCE

    assert indicator.related_observables[0].type == IP4
    assert indicator.related_observables[0].value == "2.2.2.2"
    assert indicator.related_observables[0].valid_from == FROM_TIMESTAMP
    assert indicator.related_observables[0].valid_to == TO_TIMESTAMP
    assert indicator.related_observables[0].confidence_score == LOW_CONFIDENCE

    assert indicator.related_observables[1].type == URL
    assert indicator.related_observables[1].value == "wwww.relatedUrl.com"
    assert indicator.related_observables[1].valid_from == FROM_TIMESTAMP
    assert indicator.related_observables[1].valid_to == TO_TIMESTAMP
    assert indicator.related_observables[1].confidence_score == HIGH_CONFIDENCE

    assert indicator.tags == ["importantTag", "anotherTag"]


def test_indicator_repr(indicator):
    assert indicator.__repr__() == "Indicator(value=www.badurl.com, type=URL)"
