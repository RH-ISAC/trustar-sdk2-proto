from __future__ import unicode_literals

import pytest
from trustar2.models import Indicator, Entity


@pytest.fixture
def indicator():
    return Indicator("URL", "www.badurl.com")


def test_set_related_observables(indicator):
    related_observable_email = Entity.observable("EMAIL_ADDRESS", "bob@gmail.com")
    indicator.set_related_observables(related_observable_email)
    assert related_observable_email in indicator.related_observables


def test_set_attributes(indicator):
    attributes = Entity.attribute("THREAT_ACTOR", "ActorName")
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
