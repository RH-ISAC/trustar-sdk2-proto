from __future__ import unicode_literals
from trustar2.base import fluent, Methods, ParamsSerializer, Param, get_timestamp

from datetime import datetime
from trustar2.query import Query
from trustar2.trustar_enums import ObservableTypes, SortColumns, SortOrder, AttributeTypes
from trustar2.handlers.base_handler import BaseHandler
from trustar2.handlers.indicator_tags import TagIndicator
from trustar2.models import Entity



@fluent
class SearchIndicator(BaseHandler):
    url = "/indicators"

    def __init__(self, config=None):
        super(SearchIndicator, self).__init__(config)
        self.endpoint = None


    @property
    def base_url(self):
        return self.config.request_details.get("api_endpoint") + self.url


    def _validate_dates(self):
        from_date = self.payload_params.get("from")
        to_date = self.payload_params.get("to")
        if from_date and to_date:
            from_date_dt = datetime.fromtimestamp(from_date / 1000)
            to_date_dt = datetime.fromtimestamp(to_date / 1000)
            if (to_date_dt - from_date_dt).days > 364:
                raise AttributeError("Time window can not be greater than 1 year.")

            if (from_date_dt > to_date_dt):
                raise AttributeError("'from' can not be a date after 'to'.")

        if from_date and not to_date:
            from_date_dt = datetime.fromtimestamp(from_date / 1000)
            if (datetime.today() - from_date_dt).days > 364:
                raise AttributeError("Time window can not be greater than 1 year.")

        
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


    def set_query_term(self, query):
        self.set_payload_param("queryTerm", query)


    def set_page_size(self, page_size):
        self.set_query_param("pageSize", page_size)


    def set_from(self, from_date):
        if not isinstance(from_date, int):
            from_date = get_timestamp(from_date)
        self.set_payload_param("from", from_date)


    def set_to(self, to_date):
        if not isinstance(to_date, int):
            to_date = get_timestamp(to_date)

        self.set_payload_param("to", to_date)


    def set_sort_column(self, column):
        column = self._get_value(column, SortColumns)
        self.set_payload_param("sortColumn", column)


    def set_sort_order(self, order):
        order = self._get_value(order, SortOrder)
        self.set_payload_param("sortOrder", order)


    def set_priority_scores(self, scores):
        if not isinstance(scores, list) or any([s for s in scores if s > 3 or s < -1]):
            raise AttributeError("scores should be a list of integers between -1 and 3")
        self.set_payload_param("priorityScores", scores)


    def set_enclave_ids(self, enclave_guids):
        if not isinstance(enclave_guids, list):
            enclave_guids = [enclave_guids]
        self.set_payload_param("enclaveGuids", enclave_guids)


    def set_included_tags(self, tags):
        if not isinstance(tags, list):
            tags = [tags]
        self.set_payload_param("includedTags", tags)


    def set_excluded_tags(self, tags):
        if not isinstance(tags, list):
            tags = [tags]
        self.set_payload_param("excludedTags", tags)


    def set_observable_types(self, types):
        if not isinstance(types, list):
            raise AttributeError("types should be a list")

        types = [self._get_value(t, ObservableTypes) for t in types]
        self.set_payload_param("types", types)


    def set_attributes(self, attributes):
        if not isinstance(attributes, list):
            raise AttributeError("attributes should be a list")

        attributes = [self._get_entity(e, AttributeTypes) for e in attributes]
        self.set_payload_param("attributes", attributes)


    def set_related_observables(self, observables):
        if not isinstance(observables, list):
            raise AttributeError("observables should be a list")

        observables = [self._get_entity(o, ObservableTypes) for o in observables]
        self.set_payload_param("relatedObservables", observables)


    def set_include_safelisted(self, include_safelisted):
        self.set_payload_param("includeSafelisted", include_safelisted)


    def create_query(self, method):
        return Query(self.config, self.endpoint, method)


    def search(self):
        self._validate_dates()
        self.endpoint = self.base_url + "/search"
        return (
            self.create_query(Methods.POST)
            .set_params(self.payload_params)
            .set_query_string({"pageSize": self.query_params.get("pageSize", 25)})
        )

    def tags(self):
        return TagIndicator(self.config)