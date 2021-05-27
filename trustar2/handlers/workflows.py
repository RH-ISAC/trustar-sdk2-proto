
from trustar2.base import fluent
from trustar2.handlers.base_handler import BaseHandler


@fluent
class Workflows(BaseHandler):


    def __init__(self, config=None):
        super(Workflows, self).__init__(config)
        self.workflow_guid = None


    def set_type(self, type):
        # TODO: Validations ?
        self.set_query_param("type", type)


    def set_name(self, type):
        # TODO: Validations ?
        self.set_query_param("name", type)


    def set_created_from(self, type):
        # TODO: Validations ?
        self.set_query_param("createdFrom", type)


    def set_created_to(self, type):
        # TODO: Validations ?
        self.set_query_param("createdTo", type)

    
    def set_updated_from(self, type):
        # TODO: Validations ?
        self.set_query_param("updatedFrom", type)

    
    def set_updated_to(self, type):
        # TODO: Validations ?
        self.set_query_param("updatedTo", type)


    def set_workflow_id(self, workflow_id):
        # TODO: Validations
        self.workflow_guid = workflow_id
