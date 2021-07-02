from trustar2.models import Entity
from trustar2.models.base import Base
from trustar2.models.score_context import ScoreContext


class PrioritizedIndicator(Base):

    def __init__(self, guid, enclave_guid, workflow_guid, observable, priority_score, attributes, 
                 user_tags, submission_tags, score_contexts, created, updated, processed_at, safelisted):

        self.guid = guid
        self.enclave_guid = enclave_guid
        self.workflow_guid = workflow_guid
        self.observable = observable
        self.priority_score = priority_score
        self.attributes = attributes
        self.user_tags = user_tags
        self.submission_tags = submission_tags
        self.score_contexts = score_contexts
        self.created = created
        self.updated = updated
        self.processed_at = processed_at
        self.safelisted = safelisted


    def __repr__(self):
        return "PrioritizedIndicator(type={}, value={})".format(self.observable.type, self.observable.value)


    @classmethod
    def from_dict(cls, ioc_dict):
        observable = ioc_dict.get("observable")
        observable_obj = Entity.observable(
            observable.get("type"), 
            observable.get("value")
        )

        attributes = [
            Entity.attribute(e.get("type"), e.get("value"))
            for e in ioc_dict.get("attributes")
        ]

        score_contexts = [
            ScoreContext.from_dict(sc) 
            for sc in ioc_dict.get("scoreContexts")
        ]

        return cls(
            guid=ioc_dict.get("guid"),
            enclave_guid=ioc_dict.get("enclaveGuid"),
            workflow_guid=ioc_dict.get("workflowGuid"),
            observable=observable_obj,
            priority_score=ioc_dict.get("priorityScore"),
            attributes=attributes,
            user_tags=ioc_dict.get("userTags"),
            submission_tags=ioc_dict.get("submissionTags"),
            score_contexts=score_contexts,
            created=ioc_dict.get("created"),
            updated=ioc_dict.get("updated"),
            processed_at=ioc_dict.get("processedAt"),
            safelisted=ioc_dict.get("safelisted")
        )


    def serialize(self):
        serialized = super(PrioritizedIndicator, self).serialize()
        observable = serialized.get("observable").get("entity")
        attributes = [a.get("entity") for a in serialized.get("attributes")]
        serialized.update({"observable": observable, "attributes": attributes})
        return serialized
