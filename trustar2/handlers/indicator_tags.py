from __future__ import unicode_literals

from trustar2.base import Methods, Param, ParamsSerializer, fluent
from trustar2.query import Query
from trustar2.handlers.base_handler import BaseHandler


@fluent
class TagIndicator(BaseHandler):
    url = "/indicators"

    def __init__(self, config=None):
        super(TagIndicator, self).__init__(config)
        self.ioc_guid = None

    @property
    def base_url(self):
        return self.config.request_details.get("api_endpoint") + self.url

    @property
    def tag_endpoint(self):
        if self.ioc_guid is None:
            raise AttributeError(
                "Indicator id value is required for altering tags of an indicator submission"
            )
        if "addedTags" not in self.payload_params and "removedTags" not in self.payload_params:
            raise AttributeError(
                "Either 'addedTags' or 'removedTags' values are required for altering tags of an indicator submission"
            )
        if "enclaveGuid" not in self.payload_params:
            raise AttributeError(
                "Enclave id value is required for altering tags of an indicator submission"
            )

        return self.base_url + "/{}/alter-tags".format(self.ioc_guid)

    def set_custom_param(self, key, value):
        param = Param(key=key, value=value)
        self.params.add(param)

    def set_added_tags(self, added_tags):
        if not isinstance(added_tags, list):
            raise AttributeError(u"addedTags {} should be a list of string values".format(added_tags))
        self.set_payload_param("addedTags", added_tags)

    def set_removed_tags(self, removed_tags):
        if not isinstance(removed_tags, list):
            raise AttributeError(u"removed_tags {} should be a list of string values".format(removed_tags))
        self.set_payload_param("removedTags", removed_tags)

    def set_enclave_id(self, enclave_guid):
        self.set_payload_param("enclaveGuid", enclave_guid)

    def set_indicator_id(self, indicator_id):
        self.ioc_guid = indicator_id

    def create_query(self, method, endpoint):
        return Query(self.config, endpoint, method)

    def alter_tags(self):
        endpoint = self.tag_endpoint
        return (
            self.create_query(Methods.POST, endpoint)
            .set_params(self.payload_params)
            .execute()
        )
