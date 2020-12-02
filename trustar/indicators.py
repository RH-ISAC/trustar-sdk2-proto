from __future__ import unicode_literals

import dateparser

from .base import fluent, Methods, Params, Param
from .query import Query
from .trustar_enums import ObservableTypes, SortColumns, AttributeTypes


class SearchIndicatorParamSerializer(Params):

    def serialize(self):
        return {n.key: n.value for n in self}


@fluent
class SearchIndicator:
    url = "/indicators"

    def __init__(self, config):
        self.config = config
        self.params = SearchIndicatorParamSerializer()
        self.endpoint = None

    @property
    def base_url(self):
        return self.config.request_details.get("api_endpoint") + self.url

    @property
    def tag_endpoint(self):
        if "tag" and "indicator_id" not in self.params:
            raise AttributeError("Indicator id and a tag are required for creating/deleting a new user tag")
        return self.base_url + "/{}/tags".format(self.params.get("indicator_id"))

    @staticmethod
    def _get_timestamp(date):
        dt_obj = dateparser.parse(date)
        return int(dt_obj.strftime("%s"))

    def _valid_dates(self):
        return self.params.get("from", False) and self.params.get("to", False)\
               and self.params.get("from", 0) < self.params.get("to", 0)

    def set_tag(self, tag):
        self.set_custom_param("tag", tag)

    def set_page_size(self, page_size):
        self.set_custom_param("pageSize", page_size)

    def set_custom_param(self, key, value):
        param = Param(key=key, value=value)
        self.params.add(param)

    def set_query_term(self, query):
        self.set_custom_param("queryTerm", query)

    def set_from(self, from_date):
        if not isinstance(from_date, int):
            from_date = self._get_timestamp(from_date)
        self.set_custom_param("from", from_date)

    def set_to(self, to_date):
        if not isinstance(to_date, int):
            to_date = self._get_timestamp(to_date)

        self.set_custom_param("to", to_date)

    def set_sort_column(self, column):
        if column not in SortColumns.members():
            raise AttributeError(
                "column should be one of the following: {}".format(
                    list(SortColumns.members())
                ))

        self.set_custom_param("sortColumn", column)

    def set_priority_scores(self, scores):
        if not isinstance(scores, list) or any([s for s in scores if s > 3 or s < -1]):
            raise AttributeError(
                "scores should be a list of integers between -1 and 3"
            )
        self.set_custom_param("priorityScores", scores)

    def set_enclave_ids(self, enclave_ids):
        if not isinstance(enclave_ids, list):
            enclave_ids = [enclave_ids]
        self.set_custom_param("enclaveIds", enclave_ids)

    def set_observable_types(self, types):
        if not isinstance(types, list):
            raise AttributeError("types should be a list")
        selected_types = set(types)
        valid_types = set(ObservableTypes.members())
        if not selected_types.issubset(valid_types):
            raise AttributeError(
                "observable type should be one of the following: {}".format(
                    valid_types)
                )

        self.set_custom_param("types", types)

    def set_attributes(self, attributes):
        if not isinstance(attributes, list):
            raise AttributeError("attribute should be a list")
        attribute_types = [a.get("type") for a in attributes]
        selected_attributes = set(attribute_types)
        valid_attributes = set(AttributeTypes.members())
        if not selected_attributes.issubset(valid_attributes):
            raise AttributeError(
                "attribute type should be one of the following: {}".format(
                    tuple(valid_attributes)
                ))

        self.set_custom_param("attributes", attributes)

    def set_related_observables(self, observables):
        obs_types = [o.get("type") for o in observables]
        selected_observables = set(obs_types)
        valid_observables = set(ObservableTypes.members())
        if not selected_observables.issubset(valid_observables):
            raise AttributeError(
                "observable type should be one of the following: {}".format(
                    obs_types
                ))

        self.set_custom_param("relatedObservables", observables)

    def set_indicator_id(self, indicator_id):
        self.set_custom_param("indicator_id", indicator_id)

    def create_query(self, method):
        return Query(self.config, self.endpoint, method)

    def search(self):
        # TODO check that the both the start and to are set
        if not self._valid_dates():
            raise AttributeError("Polling window should end after the start of it.")
        self.endpoint = self.base_url
        return self.create_query(Methods.POST).set_params(self.params).\
            set_query_string({"pageSize": self.params.get("pageSize", 25)})

    def create_tag(self):
        self.endpoint = self.tag_endpoint
        return self.create_query(Methods.POST).set_query_string({"tag": self.params.get("tag")}).fetch_one()

    def delete_tag(self):
        self.endpoint = self.tag_endpoint
        return self.create_query(Methods.DELETE).set_query_string({"tag": self.params.get("tag")}).fetch_one()
