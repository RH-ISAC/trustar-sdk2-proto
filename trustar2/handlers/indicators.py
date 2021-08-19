from __future__ import unicode_literals

from trustar2.query import Query
from trustar2.models import Entity
from trustar2.base import fluent, Methods
from trustar2.handlers.tags import TagIndicator
from trustar2.handlers.search_handler import SearchHandler
from trustar2.trustar_enums import (
    ObservableTypes, 
    SortOrder, 
    AttributeTypes,
    IndicatorEnum,
    SearchEnum
)

TYPE = IndicatorEnum.TYPE.value
VALUE = IndicatorEnum.VALUE.value
PAGE_SIZE = SearchEnum.PAGE_SIZE.value


@fluent
class SearchIndicator(SearchHandler):
    url = "/indicators"

    def __init__(self, config=None):
        super(SearchIndicator, self).__init__(config)
        self.endpoint = None


    @property
    def base_url(self):
        return self.config.request_details.get("api_endpoint") + self.url


    @staticmethod
    def _get_entity(entity, entity_type):
        if isinstance(entity, Entity):
            return entity.params.serialize()[entity.key]

        if isinstance(entity, dict):
            entity_type = (
                AttributeTypes
                if issubclass(entity_type, AttributeTypes)
                else ObservableTypes
            )
            return {
                TYPE: SearchIndicator._get_value(entity.get(TYPE), entity_type),
                VALUE: entity.get(VALUE),
            }

        raise AttributeError(
            "List elements should be a dictionary or the entity class"
        )


    def set_priority_scores(self, scores):
        if not isinstance(scores, list) or any([s for s in scores if s > 3 or s < -1]):
            raise AttributeError("scores should be a list of integers between -1 and 3")
        self.set_payload_param(IndicatorEnum.PRIORITY_SCORES.value, scores)


    def set_observable_types(self, types):
        if not isinstance(types, list):
            raise AttributeError("types should be a list")

        types = [self._get_value(t, ObservableTypes) for t in types]
        self.set_payload_param(IndicatorEnum.TYPES.value, types)


    def set_attributes(self, attributes):
        if not isinstance(attributes, list):
            raise AttributeError("attributes should be a list")

        attributes = [self._get_entity(e, AttributeTypes) for e in attributes]
        self.set_payload_param(IndicatorEnum.ATTRIBUTES.value, attributes)


    def set_related_observables(self, observables):
        if not isinstance(observables, list):
            raise AttributeError("observables should be a list")

        observables = [self._get_entity(o, ObservableTypes) for o in observables]
        self.set_payload_param(IndicatorEnum.RELATED_OBSERVABLES.value, observables)


    def set_include_safelisted(self, include_safelisted):
        self.set_payload_param(IndicatorEnum.INCLUDE_SAFELISTED.value, include_safelisted)


    def create_query(self, method):
        return Query(self.config, self.endpoint, method)


    def search(self):
        self._validate_dates()
        self.endpoint = self.base_url + "/search"
        return (
            self.create_query(Methods.POST)
            .set_params(self.payload_params)
            .set_query_string({PAGE_SIZE: self.query_params.get(PAGE_SIZE, 25)})
        )


    def tags(self):
        return TagIndicator(self.config)
