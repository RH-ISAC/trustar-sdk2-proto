
from base_class import Entity
from trustar_enums import AttributeTypes


class Attribute(Entity):
    def __init__(self, value, entity_type):
        super(Attribute, self).__init__(value)
        self._validate_attribute_type(entity_type)
        self._entity_type = entity_type

    def _validate_attribute_type(self, entity_type):
        if not entity_type in AttributeTypes.members():
            raise AttributeError(
                "Attribute type should be in the following: {}".format(
                    list(AttributeTypes.members())
                ))

    @property
    def entity_type(self):
        return entity_type

    
    @entity_type.setter
    def entity_type(self, entity_type):
        self._validate_attribute_type(entity_type)
        self._entity_type = entity_type
