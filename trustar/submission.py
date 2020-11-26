import dateparser

from base import fluent, Methods, Params, Param
from query import Query


class SubmissionsParamSerializer(Params):
    def serialize(self):
        return {n.key: n.value for n in self}


@fluent
class Submission(object):

    NEW_SUBMISSION_MANDATORY_FIELDS = ("title", "content", "enclaveId")
    path = "/submissions/indicators"

    def __init__(self, config):
        self.config = config
        self.params = SubmissionsParamSerializer()

    @property
    def endpoint(self):
        return self.config.request_details.get("api_endpoint") + self.path

    @staticmethod
    def _get_timestamp(date):
        dt_obj = dateparser.parse(date)
        return int(dt_obj.strftime("%s"))

    def add_custom_param(self, param):
        self.params.add(param)

    def set_id(self, submission_id):
        self.add_custom_param(Param("id", submission_id))

    def set_title(self, title):
        self.add_custom_param(Param("title", title))

    def set_content_indicators(self, indicators):
        indicators = [i.serialize() for i in indicators]
        content = {"indicators": indicators}
        self.add_custom_param(Param("content", content))

    def set_enclave_id(self, enclave_id):
        self.add_custom_param(Param("enclaveId", enclave_id))

    def set_external_id(self, external_id):
        self.add_custom_param(Param("externalId", external_id))

    def set_external_url(self, external_url):
        self.add_custom_param(Param("externalUrl", external_url))

    def set_tags(self, tags):
        self.add_custom_param(Param("tags", tags))

    def set_include_content(self, content=False):
        self.add_custom_param(Param("includeContent", content))

    def set_timestamp(self, timestamp):
        if not isinstance(timestamp, int):
            timestamp = self._get_timestamp(timestamp)

        self.add_custom_param(Param("timestamp", timestamp))

    def set_raw_content(self, raw_content):
        self.add_custom_param(Param("rawContent", raw_content))

    @property
    def query_params(self):
        return {
            p.key: p.value
            for p in self.params
            if p in ("id", "enclaveId", "includeContent")
        }

    def create_query(self, method):
        return Query(self.config, self.endpoint, method)

    def create(self):
        for k in self.NEW_SUBMISSION_MANDATORY_FIELDS:
            if k not in self.params:
                raise AttributeError("{} field should be in your submission".format(k))
        return self.create_query(Methods.POST).set_params(self.params).fetch_one()

    def delete(self):
        return (
            self.create_query(Methods.DELETE)
            .set_query_string(self.query_params)
            .fetch_one()
        )

    def get(self):
        return (
            self.create_query(Methods.GET)
            .set_query_string(self.query_params)
            .fetch_one()
        )

    def update(self):
        return (
            self.create_query(Methods.PUT)
            .set_query_string(self.query_params)
            .fetch_one()
        )
