from api_client import ApiClient
from base import Param


class Query:
    method = None
    serializer = None

    def __init__(self, trustar, endpoint, params):
        self.trustar = trustar
        self.endpoint = endpoint
        self.params = params
        self.stop = False
        self.api = ApiClient(self.trustar)
        self.api.auth()

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def _update_params_from_response(self, response):
        if response["responseMetadata"]["nextCursor"] != "":
            cursor = Param("cursor", response["responseMetadata"]["nextCursor"])
            if cursor not in self.params:
                self.params.add(cursor)
            else:
                self.params.remove(cursor)
                self.params.add(cursor)
        else:
            self.stop = True

    def next(self):
        if not self.stop:
            result = self.api.fetch(self)
            self._update_params_from_response(result.json())
            return result
        else:
            raise StopIteration
