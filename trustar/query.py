from api_client import ApiClient


class Query:
    method = None
    serializer = None
    trustar = None

    def __init__(self, endpoint, params):
        self.endpoint = endpoint
        self.params = params

    def __iter__(self):
        return self

    def __next__(self):
        api = ApiClient(self.trustar)
        while True:
            result = api.fetch(self)
            yield result
            # update params here, use serializer class?