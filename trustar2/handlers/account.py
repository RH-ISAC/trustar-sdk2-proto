from trustar2.query import Query
from trustar2.base import fluent, Methods
from trustar2.handlers.base_handler import BaseHandler


@fluent
class Account(BaseHandler):


    def __init__(self, config=None):
        super(Account, self).__init__(config)


    @property
    def endpoint(self):
        return self.config.request_details.get("api_endpoint")
        

    def create_query(self, method, specific_endpoint=""):
        """Returns a new instance of a Query object according config, endpoint and method."""
        endpoint = self.endpoint + specific_endpoint
        return Query(self.config, endpoint, method)


    def ping(self):
        return (
            self.create_query(Methods.GET, specific_endpoint="/ping")
            .execute()
        )


    def get_enclaves(self):
        return (
            self.create_query(Methods.GET, specific_endpoint="/enclaves")
            .execute()
        )
