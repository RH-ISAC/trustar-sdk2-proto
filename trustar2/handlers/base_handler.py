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
