from api_client import ApiClient


class Query:
    method = None
    serializer = None
    trustar = None

    def __init__(self, endpoint, params):
        self.endpoint = endpoint
        self.params = params
        self.iter = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        api = ApiClient(self.trustar)
        api.auth()
        result = api.fetch(self)
        if self.iter < 2:
            self.iter += 1
            return result
        else:
            raise StopIteration()
            # update params here, use serializer class?

