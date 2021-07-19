from trustar2.query import Query
from trustar2.base import fluent, Methods
from trustar2.handlers.base_handler import BaseHandler
from trustar2.models.trustar_response import TruStarResponse


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
        """Tests connectiviy against TruSTAR API."""
        result = self.create_query(Methods.GET, specific_endpoint="/ping").execute()
        return TruStarResponse(status_code=result.status_code, data={"restult": result.text})


    def get_enclaves(self):
        """Returns all user enclaves with according permissions."""
        result = self.create_query(Methods.GET, specific_endpoint="/enclaves").execute()
        return TruStarResponse(status_code=result.status_code, data=result.json())
