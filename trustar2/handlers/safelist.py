from __future__ import unicode_literals

from trustar2.base import fluent, Methods, ParamsSerializer, Param, get_timestamp
from trustar2.handlers.base_handler import BaseHandler
from trustar2.query import Query
from trustar2.trustar_enums import ObservableTypes


@fluent
class Safelist(BaseHandler): # FALTA

    summaries = "/safelist-libraries"
    details =  summaries + "/{}"
    extract = summaries + "/extract"

    def __init__(self, trustar_config=None):
        super(Safelist, self).__init__(trustar_config)
        self.library_guid = None


    @property
    def summaries_endpoint(self):
        return self.config.request_details.get("api_endpoint") + self.summaries


    @property
    def details_endpoint(self):
        return self.config.request_details.get("api_endpoint") + self.details.format(self.library_guid)


    @property
    def extract_endpoint(self):
        return self.config.request_details.get("api_endpoint") + self.extract


    def set_library_guid(self, library_guid):
        self.library_guid = library_guid


    def _verify_entry(self, entry):
        entity = entry.get("entity")
        entity_type = entry.get("type")
        if not entity or not entity_type:
            raise AttributeError("A new entry should have 'entity' and 'type' fields")

        if not isinstance(entity, type("")):
            raise AttributeError("Your entity value should be a string")

        obs_types = ObservableTypes.members()
        if entity_type not in obs_types:
            msg = "Entity type should be one of the following: {}".format(obs_types)
            raise AttributeError(msg)


    def set_safelist_entries(self, entries):
        if isinstance(entries, dict):
            entries = [entries]
        
        for entry in entries:
            self._verify_entry(entry)

        self.set_payload_param("entries", entries)


    def set_library_name(self, library_name):
        if not isinstance(library_name, type("")):
            raise AttributeError("Library name must be a string.")

        self.set_payload_param("name", library_name)

    
    def set_text_to_be_extracted(self, text):
        if not isinstance(text, type("")):
            raise AttributeError("You can only submit a text for extraction.")

        self.set_payload_param("text", text)


    def _validate_library_guid_is_present(self):
        if self.library_guid is None:
            raise AttributeError("No library guid was found.")


    def get_safelist_libraries(self):
        """Retrieves safelist details given a library guid. 

        You have to call 'set_library_guid' before calling this method.

        :returns: HTTP response with safelist library summaries in it's content.
        """
        return Query(self.config, self.summaries_endpoint, Methods.GET).set_params(self.payload_params).execute()
    

    def get_safelist_details(self):
        """Retrieves safelist details given a library guid. 

        You have to call 'set_library_guid' before calling this method.

        :returns: HTTP response with Safelist Library Details in it's content.
        """
        self._validate_library_guid_is_present()
        return Query(self.config, self.details_endpoint, Methods.GET).set_params(self.payload_params).execute()


    def create_entries(self):
        """Creates a new entry in a safelist library.

        You have to call 'set_safelist_entries' and 'set_library_guid' 
        before calling this method.

        :returns: HTTP response with Safelist Library Details in it's content.
        """
        self._validate_library_guid_is_present()
        if not self.payload_params.get("entries"):
            raise AttributeError(
                "You must call the 'set_safelist_entries' method before calling this method."
            )

        return Query(self.config, self.details_endpoint, Methods.PATCH).set_params(self.payload_params).execute()


    def create_safelist(self):
        """Creates a new safelist library with the corresponding name. 

        You have to call 'set_library_name' before calling this method. 
        
        :returns: HTTP response with safelist library summaries in it's content.
        """
        if not self.payload_params.get("name"):
            raise AttributeError(
                "You must provide a name for the new library. Call the 'set_library_name' method before."
            )

        return Query(self.config, self.summaries_endpoint, Methods.POST).set_params(self.payload_params).execute()


    def delete_entry(self, entry_guid):
        """Deletes an entry from a safelist library. 

        You have to call 'set_library_guid' before calling this method.
        
        :param entry_guid: entry guid to be deleted.
        """
        self._validate_library_guid_is_present()
        endpoint = self.details_endpoint + "/" + entry_guid
        return Query(self.config, endpoint, Methods.DELETE).set_params(self.payload_params).execute()
    

    def delete_safelist(self):
        """Deletes a safelist library. You have to call 'set_library_guid' before
        calling this method."""
        self._validate_library_guid_is_present()
        return Query(self.config, self.details_endpoint, Methods.DELETE).set_params(self.payload_params).execute()


    def extract_terms(self):
        """Extracts IOCs from unstructured text and returns a list of entities ready to be submitted. 

        You have to call 'set_text_to_be_extracted' before calling this method.

        :returns: HTTP response with parsed entities in its content.
        """
        if not self.payload_params.get("text"):
            raise AttributeError(
                "You did not set any text for entities extraction. Call 'set_text_to_be_extracted' before."
            )

        return Query(self.config, self.extract_endpoint, Methods.POST).set_params(self.payload_params).execute()
