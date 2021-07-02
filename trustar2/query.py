from .api_client import ApiClient
from .base import Param, fluent

from trustar2.models.trustar_response import TruStarResponse
from trustar2.models.searched_observable import SearchedObservable
from trustar2.models.searched_submission import SearchedSubmission
from trustar2.models.prioritized_indicator import PrioritizedIndicator

ENDPOINT_IDX = -2


@fluent
class Query:

    def __init__(self, config, endpoint, method, params=None, query_string=None):
        self.config = config
        self.endpoint = endpoint
        self.method = method
        self.params = params
        self.query_string = query_string
        self.stop = False
        self.api = ApiClient(self.config)

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def set_query_string(self, query_string):
        self.query_string = query_string

    def set_params(self, params):
        self.params = params

    def _update_cursor(self, response):
        if response["responseMetadata"].get("nextCursor", "") != "":
            cursor = Param("cursor", response["responseMetadata"]["nextCursor"])
            self.params.add(cursor)
        else:
            self.stop = True

    def _update_page(self, response):
        if response["hasNext"]:
            currentPage = int(response.get("pageNumber", 0))
            pageNumber = Param("pageNumber", currentPage + 1)
            self.params.add(pageNumber)
        else:
            self.stop = True

    def _update_params_from_response(self, response):
        if "responseMetadata" in response.keys():
            self._update_cursor(response)
        elif "hasNext" in response.keys():
            self._update_page(response)


    def _get_content_from_endpoint(self, result):
        endpoint_obj = {
            "indicators": PrioritizedIndicator, 
            "observables": SearchedObservable, 
            "submissions": SearchedSubmission
        }
        endpoint = self.endpoint.rsplit("/")[ENDPOINT_IDX]
        obj = endpoint_obj.get(endpoint)
        return [obj.from_dict(i) for i in result.json().get("items")]


    def next(self):
        if not self.stop:
            result = self.api.fetch(self, use_empty_payload=True)
            self._update_params_from_response(result.json())

            return TruStarResponse(
                status_code = result.status_code,
                data=self._get_content_from_endpoint(result)
            )

        else:
            raise StopIteration

    def execute(self, use_empty_payload=False):
        return self.api.fetch(self, use_empty_payload)
