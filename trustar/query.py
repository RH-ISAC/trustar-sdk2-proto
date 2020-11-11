from api_client import ApiClient


class Query:
    endpoint = None
    method = None
    serializer = None
    trustar = None

    def __init__(self):
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

