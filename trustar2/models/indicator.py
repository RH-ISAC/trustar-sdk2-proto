from __future__ import unicode_literals

from .base import Base
from .entity import Entity
from trustar2.base import fluent, typename
from trustar2.trustar_enums import ObservableTypes, MaxValues, IndicatorEnum


@fluent
class Indicator(Base):

    FIELD_METHOD_MAPPING = {
        "validFrom": "set_valid_from",
        "validTo": "set_valid_to",
        "maliciousScore": "set_malicious_score",
        "confidenceScore": "set_confidence_score",
        "attributes": "_set_attributes_from_dict",
        "relatedObservables": "_set_related_obs_from_dict",
        "tags": "set_tags",
        "properties": "set_properties"
    } 

    def __init__(self, entity_type, value):
        self.observable = Entity(ObservableTypes, entity_type, value, alias="observable")
        self.attributes = []
        self.related_observables = []
        self.tags = []


    def __repr__(self):
        return "{}(value={}, type={})".format(typename(self), self.observable.value, self.observable.type)
    

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
        if valid_to is not None:
            self.observable.set_valid_to(valid_to)

    def set_valid_from(self, valid_from):
        if valid_from is not None:
            self.observable.set_valid_from(valid_from)

    def set_malicious_score(self, mal_score):
        if mal_score is not None:
            self.observable.set_malicious_score(mal_score)

    def set_confidence_score(self, conf_score):
        if conf_score is not None:
            self.observable.set_confidence_score(conf_score)

    def set_properties(self, properties):
        self.observable.set_properties(properties)

    @property
    def valid_to(self):
        return self.observable.valid_to

    @property
    def valid_from(self):
        return self.observable.valid_from

    @property
    def malicious_score(self):
        return self.observable.malicious_score

    @property
    def confidence_score(self):
        return self.observable.confidence_score

    @property
    def properties(self):
        return self.observable.properties


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

        serialized.update({
            IndicatorEnum.ATTRIBUTES.value: [attr.serialize() for attr in self.attributes] 
            if len(self.attributes) else []
        })

        serialized.update({
            IndicatorEnum.RELATED_OBSERVABLES.value: [
                attr.serialize() 
                for attr in self.related_observables
            ] 
            if len(self.related_observables) else []
        })
        serialized.update({IndicatorEnum.TAGS.value: self.tags})
        return serialized


    def _set_attributes_from_dict(self, attributes):
        if len(attributes) > 0:
            self.set_attributes([Entity.from_dict(a) for a in attributes])


    def _set_related_obs_from_dict(self, observables):
        if len(observables) > 0:
            self.set_related_observables([Entity.from_dict(o) for o in observables])


    @classmethod
    def from_dict(cls, ioc_dict):
        observable = ioc_dict.pop(IndicatorEnum.OBSERVABLE.value)
        indicator = cls(observable.get(IndicatorEnum.TYPE.value), observable.get(IndicatorEnum.VALUE.value))
        
        for field, value in ioc_dict.items():
            method_name = cls.FIELD_METHOD_MAPPING.get(field)
            if method_name:
                method = getattr(indicator, method_name)
                method(value)

        return indicator
