# local imports
from enum import Enum
import requests
from .log import get_logger

logger = get_logger(__name__)


class AutoNumber(Enum):
    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


class Methods(AutoNumber):
    POST = ()
    GET = ()
    DELETE = ()
    UPDATE = ()
    PUT = ()


class ApiClient:
    """
    This class is used to make HTTP requests to the TruStar API.
    """

    def __init__(self, trustar):
        self.trustar = trustar
        self.strategies = {Methods.POST: self._post}

    def __enter__(self):
        logger.debug("Authenticating")
        yield requests.get(auth=self.trustar.auth)

    @staticmethod
    def _post(query):
        logger.debug("Posting to endpoint {}, with params {}".format(query.endpoint,
                                                                     query.params))
        return requests.post(url=query.endpoint, params=query.params)

    def fetch(self, query):
        return self.strategies[query.method]


class Param:

    def __init__(self, key, value):
        self.__key = key
        self.value = value

    def __hash__(self):
        return hash(self.__key)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.__key == other.__key

    def __str__(self):
        # TODO html escape here
        return "{}={}".format(self.key, self.value)


class Query:
    endpoint = None
    method = None
    serializer = None

    def __next__(self):
        while True:
            with ApiClient as api:
                result = self.serializer(api.fetch(self))
                yield result
                # update params here, use serializer class?


class SearchIndicator:
    endpoint = "/api/2.0/indicators/"

    params = set()

    def set_query_term(self, query=None):
        self.params.add(Param("queryTerm", query))
        return self

    def set_timestamp(self, timestamp):
        self.params.add(Param("timestamp", timestamp))
        return self

    def set_start(self, start=None):
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
        q.endpoint = self.endpoint + "&".join(self.parmas)
        q.method = Methods.POST
        q.serializer = None
        return q
