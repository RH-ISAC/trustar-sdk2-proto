from .base import Base
from .entity import Entity
from trustar.base import fluent
from trustar.trustar_enums import AttributeTypes, ObservableTypes


@fluent
class Indicator(Base):
    def __init__(self, observable, valid_to=None, valid_from=None, mal_score=None):
        self.observable = observable
        self.valid_to = valid_to
        self.valid_from = valid_from
        self.maliciousness_score = mal_score
        self.attributes = []
        self.related_observables = []
        self.tags = []

    def set_tags(self, tags):
        self.tags += tags

    def set_related_observables(self, related_obs):
        self.related_observables.append(related_obs)

    def set_attributes(self, related_attribute):
        self.attributes.append(related_attribute)
