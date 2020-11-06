from api_client import ApiClient


class Query:
    endpoint = None
    method = None
    serializer = None
    trustar = None

    def __iter__(self):
        return self

    def __next__(self):
        api = ApiClient(self.trustar)
        while True:
            result = api.fetch(self)
            yield result
            # update params here, use serializer class?