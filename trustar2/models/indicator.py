from __future__ import unicode_literals

from .base import Base
from .entity import Entity
from trustar2.base import fluent
from trustar2.trustar_enums import ObservableTypes, MaxValues


@fluent
class Indicator(Base):
    def __init__(self, entity_type, value):
        self.observable = Entity(ObservableTypes, entity_type, value, alias="observable")
        self.attributes = []
        self.related_observables = []
        self.tags = []

    def set_related_observables(self, related_obs):
        if isinstance(related_obs, list):
            self.related_observables += related_obs
        else:
            self.related_observables.append(related_obs)

        if len(self.related_observables) > MaxValues.RELATED_OBSERVABLES.value:
            self.related_observables = self.related_observables[:MaxValues.RELATED_OBSERVABLES.value]

    def set_attributes(self, related_attribute):
        if isinstance(related_attribute, list):
            self.attributes += related_attribute
        else:
            self.attributes.append(related_attribute)

        if len(self.attributes) > MaxValues.ATTRIBUTES.value:
            self.attributes = self.attributes[:MaxValues.ATTRIBUTES.value]

    def set_valid_to(self, valid_to):
        self.observable.set_valid_to(valid_to)

    def set_valid_from(self, valid_from):
        self.observable.set_valid_from(valid_from)

    def set_malicious_score(self, mal_score):
        self.observable.set_malicious_score(mal_score)

    def set_confidence_score(self, conf_score):
        self.observable.set_confidence_score(conf_score)

    def set_properties(self, properties):
        self.observable.set_properties(properties)

    def set_tags(self, tag):
        if isinstance(tag, list):
            self.tags += tag
        else:
            self.tags.append(tag)

        if len(self.tags) > MaxValues.TAGS.value:
            self.tags = self.tags[:MaxValues.TAGS.value]

    def serialize(self):
        serialized = {}
        serialized.update(self.observable.serialize())
        serialized.update({"attributes": [attr.serialize() for attr in self.attributes] if len(self.attributes) else []})
        serialized.update({"relatedObservables": [attr.serialize() for attr in self.related_observables] if len(self.related_observables) else []})
        serialized.update({"tags": self.tags})
        return serialized


    @classmethod
    def from_dict(cls, ioc_dict):
        observable = ioc_dict.get("observable")
        indicator = cls(observable.get("type"), observable.get("value"))
        valid_from = ioc_dict.get("validFrom")
        valid_to = ioc_dict.get("validTo")
        malicious_score = ioc_dict.get("maliciousScore")
        confidence_score = ioc_dict.get("confidenceScore")
        attributes = ioc_dict.get("attributes")
        related_observables = ioc_dict.get("relatedObservables")
        tags = ioc_dict.get("tags")
        properties = ioc_dict.get("properties")
        
        if valid_from is not None:
            indicator.set_valid_from(valid_from)

        if valid_to is not None:
            indicator.set_valid_to(valid_to)

        if malicious_score is not None:
            indicator.set_malicious_score(malicious_score)
        
        if confidence_score is not None:
            indicator.set_confidence_score(confidence_score)

        if len(attributes) > 0:
            indicator.set_attributes([Entity.attribute_from_dict(a) for a in attributes])

        if len(observables) > 0:
            indicator.set_related_observables([Entity.observable_from_dict(o) for o in related_observables])

        if len(tags) > 0:
            indicator.set_tags(tags)

        if properties is not None:
            indicator.set_properties(properties)

        return indicator
