from trustar2.base import typename
from trustar2.models.base import Base


class Enclave(object):


    def __init__(self, name, template_name, workflow_supported, 
                 read, create, update, id, type):
        self.name = name
        self.template_name = template_name
        self.workflow_supported = workflow_supported
        self.read = read
        self.create = create
        self.update = update
        self.id = id
        self.type = type


    def __repr__(self):
        return "{}(name={}, id={})".format(typename(self), self.name, self.id)


    @classmethod
    def from_dict(cls, enclave_dict): 
        return cls(
            name=enclave_dict.get("name"),
            template_name=enclave_dict.get("templateName"),
            workflow_supported=enclave_dict.get("workflowSupported"),
            read=enclave_dict.get("read"),
            create=enclave_dict.get("create"),
            update=enclave_dict.get("update"),
            id=enclave_dict.get("id"),
            type=enclave_dict.get("type")
        )
