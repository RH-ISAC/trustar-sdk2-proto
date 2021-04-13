
from __future__ import unicode_literals

from .base import fluent, Methods, Params, Param, get_timestamp
from .query import Query


class SafelistParamSerializer(Params):
    def serialize(self):
        return {n.key: n.value for n in self}


@fluent
class Safelist(object):

    libraries = "/safelist-libraries"
    details = "/safelist-libraries/{}"
    extract = "/safelist-libraries/extract"

    def __init__(self, trustar_config=None):
        self.config = trustar_config
        self.params = SafelistParamSerializer()
        self.enclave_guid = None


    def set_custom_param(self, key, value):
        """Adds a new param to set of params."""
        param = Param(key=key, value=value)
        self.params.add(param)


    @property
    def libraries_endpoint(self):
        return self.config.request_details.get("api_endpoint") + self.libraries

    
    @property
    def details_endpoint(self):
        return self.config.request_details.get("api_endpoint") + self.details.format(self.enclave_guid)


    def set_enclave_guid(self, enclave_guid):
        self.enclave_guid = enclave_guid
        self.set_custom_param("enclaveGuid", enclave_guid) # Probably remove?


    def set_safelist_entries(self, entries):
        # TODO: Validations
        self.set_custom_param("entries", entries)


    def set_library_name(self, library_name):
        # TODO: Validations
        self.set_custom_param("name", library_name)


    def get_safelist_libraries(self):
        return Query(self.config, self.libraries_endpoint, Methods.GET).set_params(self.params).fetch_one()
    

    def get_safelist_details(self):
        if self.enclave_guid is None:
            raise AttributeError("No enclave guid was found.")

        return Query(self.config, self.details_endpoint, Methods.GET).set_params(self.params).fetch_one()


    def create_entries(self):
        if self.enclave_guid is None:
            raise AttributeError("No enclave guid was found.")

        return Query(self.config, self.details_endpoint, Methods.PATCH).set_params(self.params).fetch_one()


    def create_safelist(self):
        return Query(self.config, self.libraries_endpoint, Methods.POST).set_params(self.params).fetch_one()


    def delete_entry(self, entry_guid):
        if self.enclave_guid is None:
            raise AttributeError("No enclave guid was found.")

        endpoint = self.details_endpoint + "/" + entry_guid
        return Query(self.config, endpoint, Methods.DELETE).set_params(self.params).fetch_one()
    

    def delete_safelist(self):
        if self.enclave_guid is None:
            raise AttributeError("No enclave guid was found.")

        return Query(self.config, self.details_endpoint, Methods.DELETE).set_params(self.params).fetch_one()
