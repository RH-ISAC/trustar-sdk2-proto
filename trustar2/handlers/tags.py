from __future__ import unicode_literals

from trustar2.query import Query
from trustar2.handlers.base_handler import BaseHandler
from trustar2.base import Methods, Param, ParamsSerializer, fluent


@fluent
class TagBase(BaseHandler):

    def __init__(self, endpoint, config=None):
        super(TagBase, self).__init__(config)
        self.guid = None
        self._url = endpoint

    @property
    def base_url(self):
        return self.config.request_details.get("api_endpoint") + "/{}".format(self._url)

    @property
    def tag_endpoint(self):
        if self.guid is None:
            raise AttributeError(
                "Id value is required for altering tags of {}".format(self._url)
            )

        if "addedTags" not in self.payload_params and "removedTags" not in self.payload_params:
            raise AttributeError(
                "Either 'addedTags' or 'removedTags' values are required for altering tags of {}".format(self._url)
            )

        if "enclaveGuid" not in self.payload_params and "enclaveId" not in self.payload_params: 
            raise AttributeError(
                "Enclave id value is required for altering tags on {}".format(self._url)
            )
            
        return self.base_url + "/{}/alter-tags".format(self.guid)


    def set_added_tags(self, added_tags):
        if not isinstance(added_tags, list):
            raise AttributeError(u"addedTags {} should be a list of string values".format(added_tags))
        self.set_payload_param("addedTags", added_tags)


    def set_removed_tags(self, removed_tags):
        if not isinstance(removed_tags, list):
            raise AttributeError(u"removed_tags {} should be a list of string values".format(removed_tags))
        self.set_payload_param("removedTags", removed_tags)


    def set_enclave_id(self, enclave_guid):
        if self._url == "submissions":
            self.set_payload_param("enclaveId", enclave_guid)
        
        else:
            self.set_payload_param("enclaveGuid", enclave_guid)

        
    def create_query(self, method, endpoint):
        return Query(self.config, endpoint, method)


    def alter_tags(self):
        endpoint = self.tag_endpoint
        return (
            self.create_query(Methods.POST, endpoint)
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
