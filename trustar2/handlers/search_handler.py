from __future__ import unicode_literals

from datetime import datetime
from trustar2.base import fluent, get_timestamp
from trustar2.handlers.base_handler import BaseHandler
from trustar2.trustar_enums import (
    SortColumns, 
    SortColumns, 
    SortOrder,
    SearchEnum
)


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
        from_date = self.payload_params.get(SearchEnum.FROM.value)
        to_date = self.payload_params.get(SearchEnum.TO.value)
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
        self.set_payload_param(SearchEnum.QUERY_TERM.value, query)


    def set_from(self, from_date):
        self.set_payload_param(SearchEnum.FROM.value, get_timestamp(from_date))


    def set_to(self, to_date):
        self.set_payload_param(SearchEnum.TO.value, get_timestamp(to_date))


    def set_enclave_ids(self, enclave_guids):
        self.set_payload_param(SearchEnum.ENCLAVE_GUIDS.value, self._argument_to_unique_list(enclave_guids))


    def set_included_tags(self, tags):
        self.set_payload_param(SearchEnum.INCLUDED_TAGS.value, self._argument_to_unique_list(tags))


    def set_excluded_tags(self, tags):
        self.set_payload_param(SearchEnum.EXCLUDED_TAGS.value, self._argument_to_unique_list(tags))
        

    def set_sort_column(self, column, options = SortColumns):
        column = self._get_value(column, options)
        self.set_payload_param(SearchEnum.SORT_COLUMN.value, column)


    def set_sort_order(self, order):
        order = self._get_value(order, SortOrder)
        self.set_payload_param(SearchEnum.SORT_ORDER.value, order)


    def set_page_size(self, page_size):
        self.set_query_param(SearchEnum.PAGE_SIZE.value, page_size)
