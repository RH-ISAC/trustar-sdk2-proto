# local imports
import requests
from base import Methods
from log import get_logger
from requests.exceptions import HTTPError, ConnectionError

logger = get_logger(__name__)


class ApiClient(object):
    """
    This class is used to make HTTP requests to the TruStar API.
    """
    INVALID_TOKEN_MESSAGES = ("Expired oauth2 access token", 
                              "Invalid oauth2 access token")

    _instance = None 
    
    def __init__(self, config):
        self.config = config
        self.strategies = {Methods.POST: self._post}
        self.token = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)

        return cls._instance

    def _refresh_token(self):
        logger.debug("Authenticating")
        if self.token is not None:
            return self.token

        client_auth = requests.auth.HTTPBasicAuth(self.config.api_key, self.config.api_secret)
        post_data = {"grant_type": "client_credentials"}
        endpoint = self.config.request_details.get("auth_endpoint")
        response = requests.post(endpoint, auth=client_auth, data=post_data, verify=True)
        response.raise_for_status()
        self.token = response.json()["access_token"]
        return self.token

    def _get_headers(self, method):
        headers = {
            "Authorization": "Bearer " + self._refresh_token(),
            "Client-Metatag": self.config.client_metatag    
        }
        
        client_type = self.config.request_details.get("client_type")
        client_version = self.config.request_details.get("client_version")

        if client_type:
            headers["Client-Type"] = client_type

        if client_version:
            headers["Client-Version"] = client_version

        if method in ("POST", "PUT"):
            headers["Content-Type"] = "application/json"

        return headers

    def _request(self, method, endpoint, payload=None, params=None):
        """
        """
        retry = self.config.request_details.get("retry")
        attempted = False
        while not attempted or retry: 
            headers = self._get_headers(method)
            try:
                response = requests.request(method=method, url=endpoint, headers=headers, json=payload)
                response.raise_for_status()
                return response

            except (ConnectionError, HTTPError) as ex:
                if self._token_is_expired(response):
                    self._refresh_token()

                elif retry and response.status_code == 429:
                    retry = self._sleep(response)

                else: 
                    message = "{} {} Error (Trace-Id: {}): {}".format(response.status_code,
                                                              "Client" if response.status_code < 500 else "Server",
                                                              self._get_trace_id(response),
                                                              reason)
                    raise HTTPError(message=message, response=response)

    def _sleep(self, response):
        """
        """
        wait_time = ceil(response.json().get('waitTime') / 1000)
        logger.debug("Waiting %d seconds until next request allowed." % wait_time)
        keep_trying = wait_time <= self.config.request_details.get("max_wait_time")
        if keep_trying:
            time.sleep(wait_time)
        
        return keep_trying

    def _get_trace_id(response):
        """
        """
        trace_id = response.headers.get('Trace-Id')
        return trace_id if trace_id is not None else None


    def _post(self, query):
        logger.debug("Posting to endpoint {}, with params {}".format(query.endpoint,
                                                                     query.params))
        payload = {n.key: n.value for n in query.params}
        return self._request("POST", query.endpoint, payload=payload)

    def _put(self, ): # params missing
        pass

    def _delete(self, ): # params missing
        pass

    def _get(self, ): # params missing
        pass

    def fetch(self, query):
        return self.strategies[query.method](query)
