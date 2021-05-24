from __future__ import unicode_literals

from trustar2.query import Query
from trustar2.trustar_enums import MaxValues
from trustar2.handlers.base_handler import BaseHandler
from trustar2.base import fluent, Methods, ParamsSerializer, Param, get_timestamp


@fluent
class Submission(BaseHandler):

    SUBMISSION_MANDATORY_FIELDS = ("title", "content", "enclaveGuid")
    path = "/submissions/indicators"

    def __init__(self, config=None):
        super(Submission, self).__init__(config)
        for func in (self.set_tags,):
            func()

    def __str__(self):
        return "Submission <{}> with external Id <{}>".format(
            self.payload_params.get("title"), 
            self.payload_params.get("externalId")
        )

    @property
    def endpoint(self):
        return self.config.request_details.get("api_endpoint") + self.path


    def set_id(self, submission_id):
        """Adds id param to set of params.

        :param submission_id: field value.
        :returns: self.
        """
        self.set_payload_param("id", submission_id)
        self.set_query_param("id", submission_id)


    def set_title(self, title):
        """Adds title param to set of params.

        :param title: field value.
        :returns: self.
        """
        self.set_payload_param("title", title)


    def set_content_indicators(self, indicators):
        """Adds content param to set of params.

        :param indicators: field value. List of Indicator objects.
        :returns: self.
        """
        indicators = [i.serialize() for i in indicators]
        if len(indicators) > MaxValues.INDICATORS.value:
            indicators = indicators[:MaxValues.INDICATORS.value]

        content = {"indicators": indicators}
        self.set_payload_param("content", content)


    def set_enclave_id(self, enclave_id):
        """Adds enclaveId param to set of params.

        :param enclave_id: field value.
        :returns: self.
        """
        self.set_payload_param("enclaveGuid", enclave_id)
        self.set_query_param("enclaveGuid", enclave_id)


    def set_external_id(self, external_id):
        """Adds externalId param to set of params.

        :param external_id: field value.
        :returns: self.
        """
        self.set_payload_param("externalId", external_id)


    def set_external_url(self, external_url):
        """Adds externalUrl param to set of params.

        :param external_url: field value.
        :returns: self.
        """
        self.set_payload_param("externalUrl", external_url)


    def set_tags(self, tags=None):
        """Adds tags param to set of params.

        :param tags: field value.
        :returns: self.
        """
        if not tags:
            tags = []

        if len(tags) > MaxValues.TAGS.value:
            tags = tags[:MaxValues.TAGS.value]

        self.set_payload_param("tags", tags)


    def set_id_type_as_external(self, external=False):
        """Sets idType to EXTERNAL if 'external' parameter is True.
        
        :param external: boolean indicating if id is external or not
        :returns: self.
        """
        if external:
            self.set_query_param("idType", "EXTERNAL")


    def set_include_content(self, content=False):
        """
        Adds includeContent param to set of params.

        :param content: field value.
        :returns: self.
        """
        self.set_query_param("includeContent", content)


    def set_timestamp(self, timestamp):
        """Adds timestamp param to set of params.

        :param timestamp: field value.
        :returns: self.
        """
        if not isinstance(timestamp, int):
            timestamp = get_timestamp(timestamp)

        self.set_payload_param("timestamp", timestamp)


    def set_raw_content(self, raw_content):
        """Adds rawContent param to set of params.

        :param raw_content: field value.
        :returns: self.
        """
        self.set_payload_param("rawContent", raw_content)


    def set_submission_version(self, version):
        """Adds submissionVersion param to set of params.

        :param version: field value.
        :returns: self.
        """
        self.set_payload_param("submissionVersion", version)


    @property
    def query_string_params(self):
        query_params = self.query_params.serialize()
        if self.should_use_external_id():
            query_params["id"] = self.payload_params.get("externalId")

        return query_params


    def should_use_external_id(self):
        """Returns True if params are set to retrieve a submission by external id"""
        return "idType" in self.query_params and "externalId" in self.payload_params


    def create_query(self, method, specific_endpoint=""):
        """Returns a new instance of a Query object according config, endpoint and method."""
        endpoint = self.endpoint + specific_endpoint
        return Query(self.config, endpoint, method)


    def _raise_without_id(self):
        if not "id" in self.query_string_params:
            raise AttributeError(
                "You need to set an id, or an external id marking the id type as external"
            )


    def delete(self):
        """Deletes a submission according to query_params set before."""
        self._raise_without_id()
        return (
            self.create_query(Methods.DELETE)
            .set_query_string(self.query_string_params)
            .execute()
        )

    def get(self):
        """Retrieves a submission according to query_params set before."""
        self._raise_without_id()
        return (
            self.create_query(Methods.GET)
            .set_query_string(self.query_string_params)
            .execute()
        )

    def upsert(self):
        """Update a submission if it already exists or create a new one if it doesn't."""
        for k in self.SUBMISSION_MANDATORY_FIELDS:
            if k not in self.payload_params:
                raise AttributeError("{} field should be in your submission".format(k))

        return (
            self.create_query(Methods.POST, specific_endpoint="/upsert")
            .set_params(self.payload_params)
            .set_query_string(self.query_string_params)
            .execute()
        )
