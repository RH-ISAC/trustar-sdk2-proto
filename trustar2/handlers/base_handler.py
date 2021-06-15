from datetime import datetime # remove
from trustar2.base import fluent, ParamsSerializer, Param


@fluent
class BaseHandler(object):

    def __init__(self, config=None):
        self.config = config
        self.payload_params = ParamsSerializer()
        self.query_params = ParamsSerializer()


    def set_payload_param(self, key, value):
        """Adds a new param to set of payload params."""
        param = Param(key=key, value=value)
        self.payload_params.add(param)


    def set_query_param(self, key, value):
        """Adds a new param to set of query params."""
        param = Param(key=key, value=value)
        self.query_params.add(param)


    def set_trustar_config(self, trustar_config):
        self.config = trustar_config


    # def _validate_dates(self):
    #     from_date = self.payload_params.get("from")
    #     to_date = self.payload_params.get("to")
    #     if from_date and to_date:
    #         from_date_dt = datetime.fromtimestamp(from_date / 1000)
    #         to_date_dt = datetime.fromtimestamp(to_date / 1000)
    #         if (to_date_dt - from_date_dt).days > 364:
    #             raise AttributeError("Time window can not be greater than 1 year.")

    #         if (from_date_dt > to_date_dt):
    #             raise AttributeError("'from' can not be a date after 'to'.")

    #     if from_date and not to_date:
    #         from_date_dt = datetime.fromtimestamp(from_date / 1000)
    #         if (datetime.today() - from_date_dt).days > 364:
    #             raise AttributeError("Time window can not be greater than 1 year.")
