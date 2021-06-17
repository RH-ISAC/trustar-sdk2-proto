from __future__ import unicode_literals

from trustar2.query import Query
from trustar2.base import fluent, Methods
from trustar2.handlers.tags import TagObservable
from trustar2.handlers.search_handler import SearchHandler
from trustar2.trustar_enums import ID_Types, ObservableTypes, TSEnum
 
@fluent
class ObservablesHandler(SearchHandler):

    _base_endpoint = "/observables"
    
    _get_from_submission_endpoint = ""
    _search_endpoint = "/search"

    def __init__(self, config=None):
        super(ObservablesHandler, self).__init__(config)

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
        query = Query(self.config, url, Methods.POST)
        return query.set_params(self.payload_params)
    
    def get_from_submission(self, submission_id, id_type = ID_Types.INTERNAL.value):
        """
        Prepare the query to get the observables from a submission.

        :param submission_id: The guid of the submission
        :param id_type (optional): 'INTERNAL' | 'EXTERNAL' | 'UNRECOGNIZED'
        :returns: Query Object.
        """
        url = "{}{}".format(self.base_url, self._get_from_submission_endpoint)
        self.set_query_param("submissionId", submission_id)
        self.set_query_param("idType", id_type)
        query = Query(self.config, url, Methods.GET)
        return query.set_query_string(self.query_params)

    def set_search_types(self, types):
        """
        Adds types to the search filters.

        :param types: Array of ObesrvableTypes Values
        :returns: self.
        """
        types = list(map(lambda t: self._get_value(t, ObservableTypes), set(types)))
        self.set_payload_param("types", types)
    
    def set_sort_column(self, column):
        """
        Specify the column to sort the search results.

        :param column: 'FIRST_SEEN' | 'LAST_SEEN'
        :returns: self.
        """
        class ObservableSortColumns(TSEnum):
            FIRST_SEEN = "FIRST_SEEN"
            LAST_SEEN = "LAST_SEEN"
        return super(ObservablesHandler, self).set_sort_column(column, ObservableSortColumns)

    def tags(self):
        """
        Returns an observable tags handler

        :returns: TagObservable handler.
        """
        return TagObservable(self.config)

    def _validate_tags_length(self):
        MAX_TAG_LENGTH = 20
        included_tags = self.payload_params.get("includedTags", [])
        excluded_tags = self.payload_params.get("excludedTags", [])
        if (len(included_tags) > MAX_TAG_LENGTH) or\
            (len(excluded_tags) > MAX_TAG_LENGTH):
            raise AttributeError("Tags are limited to {} per observable".format(MAX_TAG_LENGTH))

    def _validate_search_params(self):
        self._validate_dates()
        self._validate_tags_length()
