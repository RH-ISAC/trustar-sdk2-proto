from __future__ import unicode_literals

from trustar2.query import Query
from trustar2.handlers.base_handler import BaseHandler
from trustar2.base import Methods, fluent


@fluent
class TagBase(BaseHandler):

    def __init__(self, endpoint, config=None):
        super(TagBase, self).__init__(config)
        self.guid = None
        self._url = endpoint

    @property
    def base_url(self):
        return self.config.request_details.get("api_endpoint") + "/{}".format(self._url)

    def _validate_payload(self):
        if self.guid is None:
            raise AttributeError(
                "Id value is required for altering tags of {}".format(self._url)
            )
        
        added_tags = self.payload_params.get("addedTags", [])
        removed_tags = self.payload_params.get("removedTags", [])

        if len(added_tags) == 0 and len(removed_tags) == 0:
            raise AttributeError(
                "Either 'addedTags' or 'removedTags' values are required for altering tags of {}".format(self._url)
            )

        if "enclaveGuid" not in self.payload_params and "enclaveId" not in self.payload_params: 
            raise AttributeError(
                "Enclave id value is required for altering tags on {}".format(self._url)
            )


    @property
    def tag_endpoint(self):
        self._validate_payload()
        return self.base_url + "/{}/alter-tags".format(self.guid)

    def _validate_tags(self, tags):
        iterables = (list, tuple, set)
        if type(tags) not in iterables:
            raise AttributeError(u"addedTags {} should be a list of string values".format(tags))

    def set_added_tags(self, added_tags):
        self._validate_tags(added_tags)
        self.set_payload_param("addedTags", added_tags)


    def set_removed_tags(self, removed_tags):
        self._validate_tags(removed_tags)
        self.set_payload_param("removedTags", removed_tags)


    def set_enclave_id(self, enclave_guid):
        if self._url == "submissions":
            self.set_payload_param("enclaveId", enclave_guid)
        else:
            self.set_payload_param("enclaveGuid", enclave_guid)

    def alter_tags(self):
        return (
            Query(self.config, self.tag_endpoint, Methods.POST)
            .set_params(self.payload_params)
            .execute()
        )


@fluent
class TagIndicator(TagBase):

    def __init__(self, config=None):
        super(TagIndicator, self).__init__("indicators", config)


    def set_indicator_id(self, indicator_id):
        self.guid = indicator_id


@fluent
class TagSubmission(TagBase):

    def __init__(self, config=None):
        super(TagSubmission, self).__init__("submissions", config)


    def set_submission_id(self, submission_id):
        self.guid = submission_id


    def set_id_type_as_external(self, external):
        self.set_payload_param("idType", "EXTERNAL" if external else "INTERNAL")


@fluent
class TagObservable(TagBase):

    def __init__(self, config=None):
        super(TagObservable, self).__init__("observables", config)


    def set_observable_value(self, value):
        self.guid = value
        self.set_payload_param("observableValue", value)

    @property
    def tag_endpoint(self):
        self._validate_payload()
        return "{}{}".format(self.base_url, "/alter-tags")
