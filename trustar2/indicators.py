from __future__ import unicode_literals
from .base import fluent, Methods, ParamsSerializer, Param, get_timestamp

from .query import Query
from .trustar_enums import ObservableTypes, SortColumns, SortOrder, AttributeTypes
from .models import Entity



@fluent
class SearchIndicator:
    url = "/indicators"

    def __init__(self, config):
        self.config = config
        self.params = ParamsSerializer()
        self.endpoint = None

    @property
    def base_url(self):
        return self.config.request_details.get("api_endpoint") + self.url

    def _valid_dates(self):
        return (
            self.params.get("from", False)
            and self.params.get("to", False)
            and self.params.get("from", 0) < self.params.get("to", 0)
        )

    @staticmethod
    def _get_value(arg, enum):
        if isinstance(arg, enum):
            return arg.value

        if isinstance(arg, str) and arg in enum.members():
            return arg

        if isinstance(arg, type("")) and arg in enum.members():
            return arg  # For py2 and py3 compatibility

        raise AttributeError(
            "Possible value types are: {}".format(list(enum.members()))
        )

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
                "type": SearchIndicator._get_value(entity.get("type"), entity_type),
                "value": entity.get("value"),
            }

        raise AttributeError(
            "List elements should be a dictionary or the entity class"
        )

    def set_custom_param(self, key, value):
        param = Param(key=key, value=value)
        self.params.add(param)

    def set_query_term(self, query):
        self.set_custom_param("queryTerm", query)

    def set_page_size(self, page_size):
        self.set_custom_param("pageSize", page_size)

    def set_from(self, from_date):
        if not isinstance(from_date, int):
            from_date = get_timestamp(from_date)
        self.set_custom_param("from", from_date)

    def set_to(self, to_date):
        if not isinstance(to_date, int):
            to_date = get_timestamp(to_date)

        self.set_custom_param("to", to_date)

    def set_sort_column(self, column):
        column = self._get_value(column, SortColumns)
        self.set_custom_param("sortColumn", column)

    def set_sort_order(self, order):
        order = self._get_value(order, SortOrder)
        self.set_custom_param("sortOrder", order)

    def set_priority_scores(self, scores):
        if not isinstance(scores, list) or any([s for s in scores if s > 3 or s < -1]):
            raise AttributeError("scores should be a list of integers between -1 and 3")
        self.set_custom_param("priorityScores", scores)

    def set_enclave_ids(self, enclave_guids):
        if not isinstance(enclave_guids, list):
            enclave_guids = [enclave_guids]
        self.set_custom_param("enclaveGuids", enclave_guids)

    def set_included_tags(self, tags):
        if not isinstance(tags, list):
            tags = [tags]
        self.set_custom_param("includedTags", tags)

    def set_excluded_tags(self, tags):
        if not isinstance(tags, list):
            tags = [tags]
        self.set_custom_param("excludedTags", tags)

    def set_observable_types(self, types):
        if not isinstance(types, list):
            raise AttributeError("types should be a list")

        types = [self._get_value(t, ObservableTypes) for t in types]
        self.set_custom_param("types", types)

    def set_attributes(self, attributes):
        if not isinstance(attributes, list):
            raise AttributeError("attributes should be a list")

        attributes = [self._get_entity(e, AttributeTypes) for e in attributes]
        self.set_custom_param("attributes", attributes)

    def set_related_observables(self, observables):
        if not isinstance(observables, list):
            raise AttributeError("observables should be a list")

        observables = [self._get_entity(o, ObservableTypes) for o in observables]
        self.set_custom_param("relatedObservables", observables)

    def set_include_safelisted(self, include_safelisted):
        self.set_custom_param("includeSafelisted", include_safelisted)

    def create_query(self, method):
        return Query(self.config, self.endpoint, method)

    def search(self):
        # TODO check that the both the start and to are set
        if not self._valid_dates():
            raise AttributeError("Polling window should end after the start of it.")
        self.endpoint = self.base_url + "/search"
        return (
            self.create_query(Methods.POST)
            .set_params(self.params)
            .set_query_string({"pageSize": self.params.get("pageSize", 25)})
        )
