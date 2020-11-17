from api_client import ApiClient
from base import Param


class Query:
    method = None
    serializer = None

    def __init__(self, config, path, params):
        self.config = config
        self.endpoint = path
        self.params = params
        self.stop = False
        self.api = ApiClient(self.config)

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def _update_params_from_response(self, response):
        if response["responseMetadata"]["nextCursor"] != "":
            cursor = Param("cursor", response["responseMetadata"]["nextCursor"])
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
