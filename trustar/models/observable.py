
from base_class import Entity
from trustar_enums import ObservableTypes


class Observable(Entity):

    def __init__(self, value, entity_type):
        super(Observable, self).__init__(value)
        self._validate_observable_type(entity_type)
        self._entity_type = entity_type


    def _validate_observable_type(self, entity_type):
        if not entity_type in ObservableTypes.members():
            raise AttributeError(
                "Observable type should be in the following: {}".format(
                    list(ObservableTypes.members())
                ))

    @property
    def entity_type(self):
        return self._entity_type

    @entity_type.setter
    def entity_type(self, entity_type):
        self._validate_observable_type(entity_type)
        self._entity_type = entity_type
