from base import Methods, Param
from query import Query


class SearchIndicator:
    endpoint = "https://staging.trustar.co/api/2.0/indicators/?"

    def __init__(self, config):
        self.trustar = config
        self.params = set()

    def set_query_term(self, query):
        self.params.add(Param("queryTerm", query))
        return self

    def set_timestamp(self, timestamp):
        self.params.add(Param("timestamp", timestamp))
        return self

    def set_start(self, start):
        self.params.add(Param("start", start))
        return self

    def set_to(self, to):
        self.params.add(Param("timestamp", to))
        return self

    def set_custom_param(self, param):
        # Receives a Param object
        self.params.add(param)
        return self

    def query(self):
        # TODO check that the both the start and to are set
        q = Query()
        bottom = str("&".join(str(p) for p in self.params))
        q.endpoint = self.endpoint + bottom
        q.method = Methods.POST
        q.serializer = None
        print(q.endpoint)
        return q
