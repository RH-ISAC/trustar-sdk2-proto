from trustar2.base import typename
from trustar2.models.base import Base
from trustar2.models.workflow_configs import WorkflowConfig



class Workflow(Base):


    def __init__(self, guid, name, created, updated, workflow_config, safelist_guids):
        self.guid = guid
        self.name = name
        self.created = created
        self.updated = updated
        self.workflow_config = workflow_config
        self.safelist_guids = safelist_guids


    def __repr__(self):
        return "{}(name={}, guid={})".format(typename(self), self.name, self.guid)


    @classmethod
    def from_dict(cls, workflow_dict):
        workflow_config = workflow_dict.get("workflowConfig")
        return cls(
            guid=workflow_dict.get("guid"),
            name=workflow_dict.get("name"),
            created=workflow_dict.get("created"),
            updated=workflow_dict.get("updated"),
            workflow_config=WorkflowConfig.from_dict(workflow_config),
            safelist_guids=workflow_dict.get("safelistGuids")
        )
