from trustar2.base import typename
from trustar2.models.base import Base
from trustar2.trustar_enums import EnclaveEnum


class Enclave(Base):


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
            name=enclave_dict.get(EnclaveEnum.NAME.value),
            template_name=enclave_dict.get(EnclaveEnum.TEMPLATE_NAME.value),
            workflow_supported=enclave_dict.get(EnclaveEnum.WORKFLOW_SUPPORTED.value),
            read=enclave_dict.get(EnclaveEnum.READ.value),
            create=enclave_dict.get(EnclaveEnum.CREATE.value),
            update=enclave_dict.get(EnclaveEnum.UPDATE.value),
            id=enclave_dict.get(EnclaveEnum.ID.value),
            type=enclave_dict.get(EnclaveEnum.TYPE.value)
        )
