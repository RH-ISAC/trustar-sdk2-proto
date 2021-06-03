from trustar2.query import Query
from trustar2.handlers.base_handler import BaseHandler
from trustar2.base import fluent, Methods, get_timestamp



@fluent
class Workflows(BaseHandler):

    _path = "/workflows"

    def __init__(self, config=None):
        super(Workflows, self).__init__(config)
        self.workflow_guid = None


    @property
    def endpoint(self):
        return self.config.request_details.get("api_endpoint") + self._path


    def set_type(self, type):
        self.set_query_param("type", type)


    def set_name(self, name):
        if len(name) < 3 or len(name) > 120:
            raise AttributeError("Workflow name's length must be between 3 and 120 characters")

        self.set_query_param("name", name)
        self.set_payload_param("name", name)


    def set_created_from(self, created_from):
        if not isinstance(created_from, int):
            created_from = get_timestamp(created_from)

        self.set_query_param("createdFrom", created_from)


    def set_created_to(self, created_to):
        if not isinstance(created_to, int):
            created_to = get_timestamp(created_to)

        self.set_query_param("createdTo", created_to)

    
    def set_updated_from(self, updated_from):
        if not isinstance(updated_from, int):
            updated_from = get_timestamp(updated_from)

        self.set_query_param("updatedFrom", updated_from)

    
    def set_updated_to(self, updated_to):
        if not isinstance(updated_to, int):
            updated_to = get_timestamp(updated_to)

        self.set_query_param("updatedTo", updated_to)


    def set_workflow_id(self, workflow_id):
        if not isinstance(workflow_id, str):
            raise AttributeError("Workflow ID must be a string.")

        self.workflow_guid = workflow_id


    def set_workflow_config(self, workflow_config):
        self.set_payload_param("workflowConfig", workflow_config.serialize())

    
    def set_safelist_ids(self, safelist_ids):
        if not isinstance(safelist_ids, list):
            raise AttributeError("'safelist_ids' must be a list of safelist_guids (strings).")

        self.set_payload_param("safelistGuids", safelist_ids)


    def create_query(self, method, specific_endpoint=""):
        """Returns a new instance of a Query object according config, endpoint and method."""
        endpoint = self.endpoint + specific_endpoint
        return Query(self.config, endpoint, method)


    def _raise_if_payload_is_not_set_up(self):
        name = self.payload_params.get("name")
        workflow_config = self.payload_params.get("workflowConfig")
        safelist = self.payload_params.get("safelistGuids")
        if name is None or workflow_config is None or safelist is None:
            raise AttributeError("You have to set the name, workflow_config and safelist_ids for the workflow.")


    def _raise_if_workflow_id_is_not_set_up(self):
        if self.workflow_guid is None:
            raise AttributeError("You have to set up the workflow id.")

    
    def create(self):
        """
        Creates a new workflow in TruSTAR platform.
        
        You'll need to call 'set_name', 'set_workflow_config' and 'set_safelist_ids' before 
        calling to this method.
        """
        self._raise_if_payload_is_not_set_up()
        return self.create_query(Methods.POST).set_params(self.payload_params).execute()


    def get(self):
        """
        Gets all workflows in TruSTAR platform.
        You can optionally call any of the following methods to filter the results:
            - set_type
            - set_name
            - set_created_from
            - set_created_to
            _ set_updated_from
            - set_updated_to
        """
        return (
            self.create_query(Methods.GET)
            .set_query_string(self.query_params.serialize())
            .set_params(self.payload_params)
            .execute()
        )


    def get_by_id(self):
        """Gets a specific workflow by ID in TruSTAR platform.
        You'll need to call to 'set_workflow_id' before calling this method.
        """
        self._raise_if_workflow_id_is_not_set_up()
        return (
            self.create_query(Methods.GET, "/{}".format(self.workflow_guid))
            .set_params(self.payload_params)
            .execute()
        )


    def delete(self):
        """Deletes a specific workflow by ID in TruSTAR platform.
        You'll need to call to 'set_workflow_id' before calling this method.
        """
        self._raise_if_workflow_id_is_not_set_up()
        return (
            self.create_query(Methods.DELETE, "/{}".format(self.workflow_guid))
            .set_params(self.payload_params)
            .execute()
        )


    def update(self):
        """Updates a workflow in TruSTAR platform.
        
        You'll need to call to the following methods calling to this method: 
            - set_name
            - set_workflow_config
            - set_safelist_ids
            - set_workflow_id
        """
        self._raise_if_payload_is_not_set_up()
        self._raise_if_workflow_id_is_not_set_up()
        return (
            self.create_query(Methods.PUT, "/{}".format(self.workflow_guid))
            .set_params(self.payload_params)
            .execute()
        )
