from __future__ import unicode_literals

from datetime import datetime
from trustar2.base import fluent, get_timestamp
from trustar2.trustar_enums import  SortColumns
from trustar2.handlers.base_handler import BaseHandler


@fluent
class SearchHandler(BaseHandler):

    def __init__(self, config=None):
        super(SearchHandler, self).__init__(config)


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


    def set_query_term(self, query):
        self.set_payload_param("queryTerm", query)


    def set_from(self, from_date):
        if not isinstance(from_date, int):
            from_date = get_timestamp(from_date)
        self.set_payload_param("from", from_date)


    def set_to(self, to_date):
        if not isinstance(to_date, int):
            to_date = get_timestamp(to_date)

        self.set_payload_param("to", to_date)


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
        

    def set_sort_column(self, column):
        column = self._get_value(column, SortColumns)
        self.set_payload_param("sortColumn", column)
