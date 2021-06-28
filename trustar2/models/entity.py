from __future__ import unicode_literals

from .base import Base
from trustar2.base import fluent, ParamsSerializer, Param, get_timestamp
from trustar2.trustar_enums import AttributeTypes, ObservableTypes



@fluent
class Entity(Base):

    def __init__(self, validator, entity_type, value, alias='entity'):
        self.params = ParamsSerializer()
        self.validator = validator
        if entity_type not in validator.members():
            raise AttributeError(
                "Attribute type should be in the following: {}".format(
                    list(validator.members())
                ))
        self.key = alias
        self.set_custom_param(self.key, {"value": value, "type": entity_type})


    def __str__(self):
        entity = "Observable" if isinstance(self.validator, ObservableTypes) else "Attribute"
        return "{}(type={}, value={})".format(entity, self.type, self.value)


    def __repr__(self):
        return str(self)


    @classmethod
    def attribute(cls, entity_type, value):
        return Entity(AttributeTypes, entity_type, value)

    @classmethod
    def observable(cls, entity_type, value):
        return Entity(ObservableTypes, entity_type, value)

    @property
    def type(self):
        return self.params.get("entity").get("type")

    @property
    def value(self):
        return self.params.get("entity").get("value")

    def set_valid_from(self, valid_from):
        if not isinstance(valid_from, int):
            valid_from = get_timestamp(valid_from)

        self.set_custom_param("validFrom", valid_from)

    def set_valid_to(self, valid_to):
        if not isinstance(valid_to, int):
            valid_to = get_timestamp(valid_to)
        self.set_custom_param("validTo", valid_to)

    def set_confidence_score(self, confidence_score):
        # TODO validations
        self.set_custom_param("confidenceScore", confidence_score)

    def set_malicious_score(self, malicious_score):
        self.set_custom_param("maliciousScore", malicious_score)

    def set_properties(self, properties):
        if len(properties) > 20:
            raise AttributeError("properties field can not have more than 20 elements")

        for k, v in properties.items():
            if not isinstance(k, type("")) or not isinstance(v, type("")): # py2 / py3 compatibility
                raise AttributeError("Both key and value of the properties should be strings.")

        self.set_custom_param("properties", properties)

    def set_custom_param(self, key, value):
        param = Param(key=key, value=value)
        self.params.add(param)

    def serialize(self):
        return self.params.serialize()


    @classmethod
    def attribute_from_dict(cls, attr_dict):
        entity = attr_dict.get("entity")
        attribute_obj = cls.attribute(entity.get("type"), entity.get("value"))

        valid_from = attr_dict.get("validFrom")
        valid_to = attr_dict.get("validTo")
        confidence_score = attr_dict.get("confidenceScore")

        if valid_from is not None:
            self.set_valid_from(valid_from)

        if valid_to is not None:
            self.set_valid_to(valid_to)

        if confidence_score is not None:
            self.set_confidence_score(confidence_score)

        return attribute_obj


    @classmethod
    def observable_from_dict(cls, obs_dict):
        entity = obs_dict.get("entity")
        observable_obj = cls.observable(entity.get("type"), entity.get("value"))

        valid_from = obs_dict.get("validFrom")
        valid_to = obs_dict.get("validTo")
        confidence_score = obs_dict.get("confidenceScore")

        if valid_from is not None:
            self.set_valid_from(valid_from)

        if valid_to is not None:
            self.set_valid_to(valid_to)

        if confidence_score is not None:
            self.set_confidence_score(confidence_score)

        return observable_obj
