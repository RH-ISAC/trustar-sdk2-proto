
from base import fluent, Methods, Params, Param
from query import Query
from trustar_enums import ObservableTypes, SortColumns, AttributeTypes

class SubmissionsParamSerializer(Params):

    def serialize(self):
        return {n.key: n.value for n in self.map}


@fluent
class Submission(object):
    endpoint = "/submissions/indicators"

    def __init__(self, config):
        self.config = config
        self.params = SubmissionsParamSerializer()


    def add_custom_param(self, param):
        self.params.add(param)


    def set_title(self, title):
        self.add_custom_param(Param("title", title))
        
    def set_content_indicators(self, indicators):
        indicators = [i.serialize() for i in indicators]
        content = {"indicators": indicators}
        self.add_custom_param(Param("content": content))

    def set_enclave_id(self, enclave_id):
        self.add_custom_param(Param("enclaveId", enclave_id))

    def set_external_id(self, external_id):
        self.add_custom_param(Param("externalId", external_id))

    def set_external_url(self, external_url):
        self.add_custom_param(Param("externalUrl", external_url))

    def set_tags(self, tags):
        self.add_custom_param(Param("tags", tags))
    