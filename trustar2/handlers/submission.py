from __future__ import unicode_literals

from trustar2.query import Query
from trustar2.handlers.tags import TagSubmission
from trustar2.handlers.search_handler import SearchHandler
from trustar2.models.trustar_response import TruStarResponse
from trustar2.base import fluent, Methods, get_timestamp, typename
from trustar2.trustar_enums import MaxValues, SubmissionEnum, SearchEnum
from trustar2.models.submission_details import (
    StructuredSubmissionDetails, 
    UnstructuredSubmissionDetails
)

PAGE_SIZE = SearchEnum.PAGE_SIZE.value


@fluent
class Submission(SearchHandler):

    SUBMISSION_MANDATORY_FIELDS = ("title", "content", "enclaveGuid")
    _path = "/submissions"
    _submission_category = "/indicators"

    def __init__(self, config=None):
        super(Submission, self).__init__(config)
        self.set_tags()
        self.set_include_content()

    def __repr__(self):
        return "{}(title={}, external_id={})".format(
            typename(self),
            self.payload_params.get(SubmissionEnum.TITLE.value), 
            self.payload_params.get(SubmissionEnum.EXTERNAL_ID.value)
        )

    @property
    def endpoint(self):
        return self.config.request_details.get("api_endpoint") + self._path


    def set_id(self, submission_id):
        """Adds id param to set of params.

        :param submission_id: field value.
        :returns: self.
        """
        self.set_payload_param(SubmissionEnum.ID.value, submission_id)
        self.set_query_param(SubmissionEnum.ID.value, submission_id)


    def set_title(self, title):
        """Adds title param to set of params.

        :param title: field value.
        :returns: self.
        """
        self.set_payload_param(SubmissionEnum.TITLE.value, title)


    def set_content_indicators(self, indicators):
        """Adds content param to set of params.

        :param indicators: field value. List of Indicator objects.
        :returns: self.
        """
        self._submission_category = "/indicators"
        indicators = [i.serialize() for i in indicators]
        if len(indicators) > MaxValues.INDICATORS.value:
            indicators = indicators[:MaxValues.INDICATORS.value]

        content = {"indicators": indicators}
        self.set_payload_param(SubmissionEnum.CONTENT.value, content)


    def set_content_events(self, content):
        """Adds content param to set of params.

        :param indicators: field value. List of Indicator objects.
        :returns: self.
        """
        self._submission_category = "/events"
        self.set_payload_param(SubmissionEnum.CONTENT.value, content)


    def set_content_intelligence(self, content):
        """Adds content param to set of params.

        :param indicators: field value. List of Indicator objects.
        :returns: self.
        """
        self._submission_category = "/intelligence"
        self.set_payload_param(SubmissionEnum.CONTENT.value, content)


    def set_enclave_id(self, enclave_id):
        """Adds enclaveId param to set of params.

        :param enclave_id: field value.
        :returns: self.
        """
        self.set_payload_param(SubmissionEnum.ENCLAVE_GUID.value, enclave_id)
        self.set_query_param(SubmissionEnum.ENCLAVE_GUID.value, enclave_id)


    def set_external_id(self, external_id):
        """Adds externalId param to set of params.

        :param external_id: field value.
        :returns: self.
        """
        self.set_payload_param(SubmissionEnum.EXTERNAL_ID.value, external_id)


    def set_external_url(self, external_url):
        """Adds externalUrl param to set of params.

        :param external_url: field value.
        :returns: self.
        """
        self.set_payload_param(SubmissionEnum.EXTERNAL_URL.value, external_url)


    def set_tags(self, tags=None):
        """Adds tags param to set of params.

        :param tags: field value.
        :returns: self.
        """
        if not tags:
            tags = []

        if len(tags) > MaxValues.TAGS.value:
            tags = tags[:MaxValues.TAGS.value]

        self.set_payload_param(SubmissionEnum.TAGS.value, tags)


    def set_id_type_as_external(self, external=False):
        """Sets idType to EXTERNAL if 'external' parameter is True.
        
        :param external: boolean indicating if id is external or not
        :returns: self.
        """
        if external:
            self.set_query_param(SubmissionEnum.ID_TYPE.value, "EXTERNAL")


    def set_include_content(self, content=True):
        """
        Adds includeContent param to set of params.

        :param content: field value.
        :returns: self.
        """
        self.set_query_param(SubmissionEnum.INCLUDE_CONTENT.value, content)


    def set_timestamp(self, timestamp):
        """Adds timestamp param to set of params.

        :param timestamp: field value.
        :returns: self.
        """
        if not isinstance(timestamp, int):
            timestamp = get_timestamp(timestamp)

        self.set_payload_param(SubmissionEnum.TIMESTAMP.value, timestamp)


    def set_raw_content(self, raw_content):
        """Adds rawContent param to set of params.

        :param raw_content: field value.
        :returns: self.
        """
        self.set_payload_param(SubmissionEnum.RAW_CONTENT.value, raw_content)


    def set_submission_version(self, version):
        """Adds submissionVersion param to set of params.

        :param version: field value.
        :returns: self.
        """
        self.set_payload_param(SubmissionEnum.SUBMISSION_VERSION.value, version)


    @property
    def query_string_params(self):
        query_params = self.query_params.serialize()
        if self.should_use_external_id():
            query_params[
                SubmissionEnum.ID.value
            ] = self.payload_params.get(SubmissionEnum.EXTERNAL_ID.value)

        return query_params


    def should_use_external_id(self):
        """Returns True if params are set to retrieve a submission by external id"""
        return (SubmissionEnum.ID_TYPE.value in self.query_params and 
                SubmissionEnum.EXTERNAL_ID.value in self.payload_params)


    def create_query(self, method, specific_endpoint=""):
        """Returns a new instance of a Query object according config, endpoint and method."""
        endpoint = self.endpoint + specific_endpoint
        return Query(self.config, endpoint, method)


    def _raise_without_id(self):
        if not SubmissionEnum.ID.value in self.query_string_params:
            raise AttributeError(
                "You need to set an id, or an external id marking the id type as external"
            )


    def delete(self):
        """Deletes a submission according to query_params set before."""
        self._raise_without_id()
        result = (
            self.create_query(Methods.DELETE, specific_endpoint=self._submission_category)
            .set_query_string(self.query_string_params)
            .execute()
        )
        return TruStarResponse(status_code=result.status_code, data=result.content)


    def get(self, structured_indicators=True):
        """Retrieves a submission according to query_params set before."""
        self._submission_category = "/events" if not structured_indicators else "/indicators"
        self._raise_without_id()
        result = (
            self.create_query(Methods.GET, specific_endpoint=self._submission_category)
            .set_query_string(self.query_string_params)
            .execute()
        )
        Submission = StructuredSubmissionDetails if structured_indicators else UnstructuredSubmissionDetails
        return TruStarResponse(
            status_code=result.status_code, 
            data=(
                Submission.from_dict(result.json()) 
                if result.status_code < 400 and self.query_params.get(SubmissionEnum.INCLUDE_CONTENT.value) 
                else result.json()
            )
        )


    def upsert(self):
        """Update a submission if it already exists or create a new one if it doesn't."""
        for k in self.SUBMISSION_MANDATORY_FIELDS:
            if k not in self.payload_params:
                raise AttributeError("{} field should be in your submission".format(k))

        result = (
            self.create_query(Methods.POST, specific_endpoint=self._submission_category + "/upsert")
            .set_params(self.payload_params)
            .set_query_string(self.query_string_params)
            .execute()
        )
        return TruStarResponse(status_code=result.status_code, data=result.json())


    def search(self):
        """Search for submissions (intel, events and indicators)"""
        self._validate_dates()
        endpoint = "/search"
        return (
            self.create_query(Methods.POST, specific_endpoint=endpoint)
            .set_params(self.payload_params)
            .set_query_string({PAGE_SIZE: self.query_params.get(PAGE_SIZE, 25)})
        )


    def get_submission_status(self, submission_id):
        """Returns submission status for a given submission id"""
        endpoint = "/{}/status".format(submission_id)
        result = self.create_query(Methods.GET, specific_endpoint=endpoint).execute()
        return TruStarResponse(status_code=result.status_code, data=result.json())


    def tags(self):
        """Returns a TagSubmission handler that will let you alter-tags on a submission"""
        return TagSubmission(self.config)

    def set_sort_order(self, order):
        raise NotImplementedError("Submissions dont support sort order")
