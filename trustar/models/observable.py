from base import Entity
from trustar.trustar_enums import ObservableTypes


class Observable(Entity):

    def __init__(self, value, entity_type):
        super(Observable, self).__init__(value)
        self._validate_observable_type(entity_type)
        self._entity_type = entity_type

    @staticmethod
    def _validate_observable_type(entity_type):
        if entity_type not in ObservableTypes.members():
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
