from __future__ import unicode_literals

from trustar2.query import Query
from trustar2.base import fluent, Methods
from trustar2.handlers.tags import TagObservable
from trustar2.handlers.search_handler import SearchHandler
from trustar2.trustar_enums import (
    ID_Types, ObservableSortColumns, ObservableTypes, 
    MaxValues, ObservablesEnum, SearchEnum
)


MAX_TAGS = MaxValues.TAGS.value 


@fluent
class Observables(SearchHandler):

    _base_endpoint = "/observables"
    
    _get_from_submission_endpoint = ""
    _search_endpoint = "/search"

    def __init__(self, config=None):
        super(Observables, self).__init__(config)

    @property
    def base_url(self):
        return self.config.request_details.get("api_endpoint") + self._base_endpoint


    def search(self):
        """
        Prepare the query to search the observables with the specified filters.

        :returns: Query Object.
        """
        self._validate_search_params()
        url = "{}{}".format(self.base_url, self._search_endpoint)
        query = Query(self.config, url, Methods.POST, query_string=self.query_params.serialize())
        return query.set_params(self.payload_params)


    def get_from_submission(self, submission_id, id_type = ID_Types.INTERNAL.value):
        """
        Prepare the query to get the observables from a submission.

        :param submission_id: The guid of the submission
        :param id_type (optional): 'INTERNAL' | 'EXTERNAL' | 'UNRECOGNIZED'
        :returns: Query Object.
        """
        url = "{}{}".format(self.base_url, self._get_from_submission_endpoint)
        self.set_query_param(ObservablesEnum.SUBMISSION_ID.value, submission_id)
        self.set_query_param(ObservablesEnum.ID_TYPE.value, id_type)
        query = Query(self.config, url, Methods.GET)
        return query.set_query_string(self.query_params)


    def set_search_types(self, types):
        """
        Adds types to the search filters.

        :param types: Array of ObservableTypes Values
        :returns: self.
        """
        types = self._argument_to_unique_list(types)
        types = list(map(lambda t: self._get_value(t, ObservableTypes), types))
        self.set_payload_param(ObservablesEnum.TYPES.value, types)


    def set_sort_column(self, column):
        """
        Specify the column to sort the search results.

        :param column: 'FIRST_SEEN' | 'LAST_SEEN'
        :returns: self.
        """
        return super(Observables, self).set_sort_column(column, ObservableSortColumns)


    def tags(self):
        """
        Returns an observable tags handler

        :returns: TagObservable handler.
        """
        return TagObservable(self.config)


    def _validate_tags_length(self):
        included_tags = self.payload_params.get(SearchEnum.INCLUDED_TAGS.value, [])
        excluded_tags = self.payload_params.get(SearchEnum.EXCLUDED_TAGS.value, [])
        are_too_may_tags = (len(included_tags) > MAX_TAGS) or (len(excluded_tags) > MAX_TAGS)
        if are_too_may_tags:
            raise AttributeError("Tags are limited to {} per observable".format(MAX_TAGS))


    def _validate_search_params(self):
        self._validate_dates()
        self._validate_tags_length()
