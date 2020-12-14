from __future__ import unicode_literals

from .base import Base
from trustar.base import Params, Param


class EntitySerializer(Params):
    def serialize(self):
        return {n.key: n.value for n in self}


class Entity(Base):

    def __init__(self, validator, entity_type, value):
        self.params = EntitySerializer()
        if entity_type not in validator.members():
            raise AttributeError(
                "Attribute type should be in the following: {}".format(
                    list(validator.members())
                ))
        self.key = str(validator)
        self.set_custom_param(self.key, {"value": value, "type": entity_type})

    def set_valid_from(self, valid_from):
        # TODO validations
        self.set_custom_param("validFrom", valid_from)

    def set_valid_to(self, valid_to):
        # TODO validations
        self.set_custom_param("validTo", valid_to)

    def set_confidence_score(self, confidence_score):
        # TODO validations
        self.set_custom_param("confidenceScore", confidence_score)

    def set_malicious_score(self, malicious_score):
        self.set_custom_param("malicious_score", malicious_score)

    def set_custom_param(self, key, value):
        param = Param(key=key, value=value)
        self.params.add(param)
