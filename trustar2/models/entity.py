from __future__ import unicode_literals

from .base import Base
from trustar2.base import fluent, ParamsSerializer, Param, get_timestamp
from trustar2.trustar_enums import AttributeTypes, ObservableTypes



@fluent
class Entity(Base):

    FIELD_METHOD_MAPPING = {
        "validFrom": "set_valid_from",
        "validTo": "set_valid_to",
        "confidenceScore": "set_confidence_score",
    } 
    VALID_TYPES = list(AttributeTypes.members()) + list(ObservableTypes.members())


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


    def __repr__(self):
        entity = "Observable" if isinstance(self.validator, ObservableTypes) else "Attribute"
        return "{}(type={}, value={})".format(entity, self.type, self.value)


    @classmethod
    def attribute(cls, entity_type, value):
        return Entity(AttributeTypes, entity_type, value)


    @classmethod
    def observable(cls, entity_type, value):
        return Entity(ObservableTypes, entity_type, value)


    @property
    def type(self):
        return self.params.get(self.key).get("type")


    @property
    def value(self):
        return self.params.get(self.key).get("value")


    @property
    def valid_to(self):
        return self.params.get("validTo")


    @property
    def valid_from(self):
        return self.params.get("validFrom")


    @property
    def malicious_score(self):
        return self.params.get("maliciousScore")


    @property
    def confidence_score(self):
        return self.params.get("confidenceScore")


    @property
    def properties(self):
        return self.params.get("properties")


    def set_valid_from(self, valid_from):
        if valid_from is not None:
            valid_from = get_timestamp(valid_from) if not isinstance(valid_from, int) else valid_from
            self.set_custom_param("validFrom", valid_from)


    def set_valid_to(self, valid_to):
        if valid_to is not None:
            valid_to = get_timestamp(valid_to) if not isinstance(valid_to, int) else valid_to
            self.set_custom_param("validTo", valid_to)


    def set_confidence_score(self, confidence_score):
        if confidence_score is not None:
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
    def _get_entity_obj(cls, entity_type, entity):
        return (
            cls.attribute(entity_type, entity.get("value"))
            if entity_type in AttributeTypes.members()
            else cls.observable(entity_type, entity.get("value"))
        )


    @classmethod
    def from_dict(cls, entity_dict):
        entity = entity_dict.pop("entity")
        entity_type = entity.get("type")
        if entity_type not in cls.VALID_TYPES:
            raise AttributeError("Entity type does not correspond to a valid entity type")

        entity_obj = cls._get_entity_obj(entity_type, entity)
        for field, value in entity_dict.items():
            method_name = cls.FIELD_METHOD_MAPPING.get(field)
            if method_name:
                method = getattr(entity_obj, method_name)
                method(value)

        return entity_obj
