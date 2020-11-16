# local imports
import requests
from base import Methods
from log import get_logger

logger = get_logger(__name__)


class ApiClient:
    """
    This class is used to make HTTP requests to the TruStar API.
    """

    def __init__(self, trustar):
        self.trustar = trustar
        self.strategies = {Methods.POST: self._post}

    def auth(self):
        logger.debug("Authenticating")
        client_auth = requests.auth.HTTPBasicAuth(self.trustar.api_key, self.trustar.api_secret)
        # make request
        post_data = {"grant_type": "client_credentials"}
        response = requests.post(self.trustar.request_details.get("auth_endpoint"), auth=client_auth, data=post_data, verify=True)
        self.last_response = response
        self.token = response.json()["access_token"]

    def _post(self, query):
        logger.debug("Posting to endpoint {}, with params {}".format(query.endpoint,
                                                                     query.params))
        headers = {"Authorization": "Bearer " + self.token, "Content-type": "application/json"}
        return requests.post(url=query.endpoint, headers=headers, json=query.params.serialize())

    def fetch(self, query):
        return self.strategies[query.method](query)
