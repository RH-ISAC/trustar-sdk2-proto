from __future__ import unicode_literals

from .base import Methods, Param, ParamsSerializer, fluent
from .query import Query


@fluent
class TagIndicator:
    url = "/indicators"

    def __init__(self, config):
        self.config = config
        self.params = ParamsSerializer()
        self.endpoint = None

    @property
    def base_url(self):
        return self.config.request_details.get("api_endpoint") + self.url

    @property
    def tag_endpoint(self):
        if "indicator_id" not in self.params:
            raise AttributeError(
                "Indicator id value is required for altering tags of an indicator submission"
            )
        if "addedTags" not in self.params and "removedTags" not in self.params:
            raise AttributeError(
                "Either 'addedTags' or 'removedTags' values are required for altering tags of an indicator submission"
            )
        if "enclaveGuid" not in self.params:
            raise AttributeError(
                "Enclave id value is required for altering tags of an indicator submission"
            )

        return self.base_url + "/{}/alter-tags".format(self.params.get("indicator_id"))

    def set_custom_param(self, key, value):
        param = Param(key=key, value=value)
        self.params.add(param)

    def set_added_tags(self, added_tags):
        if not isinstance(added_tags, list):
            raise AttributeError(u"addedTags {} should be a list of string values".format(added_tags))
        self.set_custom_param("addedTags", added_tags)

    def set_removed_tags(self, removed_tags):
        if not isinstance(removed_tags, list):
            raise AttributeError(u"removed_tags {} should be a list of string values".format(removed_tags))
        self.set_custom_param("removedTags", removed_tags)

    def set_enclave_id(self, enclave_guid):
        self.set_custom_param("enclaveGuid", enclave_guid)

    def set_indicator_id(self, indicator_id):
        self.set_custom_param("indicator_id", indicator_id)

    def create_query(self, method):
        return Query(self.config, self.endpoint, method)

    def alter_tags(self):
        self.endpoint = self.tag_endpoint
        return (
            self.create_query(Methods.POST)
            .set_params(self.params)
            .fetch_one()
        )
