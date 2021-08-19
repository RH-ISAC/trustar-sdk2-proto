from trustar2.base import typename
from trustar2.models import Entity
from trustar2.models.base import Base
from trustar2.trustar_enums import IndicatorEnum
from trustar2.models.score_context import ScoreContext

OBSERVABLE = IndicatorEnum.OBSERVABLE.value
ATTRIBUTES = IndicatorEnum.ATTRIBUTES.value
TYPE = IndicatorEnum.TYPE.value
VALUE = IndicatorEnum.VALUE.value


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
        return "{}(type={}, value={})".format(typename(self), self.observable.type, self.observable.value)


    @classmethod
    def from_dict(cls, ioc_dict):
        observable = ioc_dict.get(OBSERVABLE)
        observable_obj = Entity.observable(
            observable.get(TYPE), 
            observable.get(VALUE)
        )

        attributes = [
            Entity.attribute(e.get(TYPE), e.get(VALUE))
            for e in ioc_dict.get(ATTRIBUTES)
        ]

        score_contexts = [
            ScoreContext.from_dict(sc) 
            for sc in ioc_dict.get(IndicatorEnum.SCORE_CONTEXTS.value)
        ]

        return cls(
            guid=ioc_dict.get(IndicatorEnum.GUID.value),
            enclave_guid=ioc_dict.get(IndicatorEnum.ENCLAVE_GUID.value),
            workflow_guid=ioc_dict.get(IndicatorEnum.WORKFLOW_GUID.value),
            observable=observable_obj,
            priority_score=ioc_dict.get(IndicatorEnum.PRIORITY_SCORE.value),
            attributes=attributes,
            user_tags=ioc_dict.get(IndicatorEnum.USER_TAGS.value),
            submission_tags=ioc_dict.get(IndicatorEnum.SUBMISSION_TAGS.value),
            score_contexts=score_contexts,
            created=ioc_dict.get(IndicatorEnum.CREATED.value),
            updated=ioc_dict.get(IndicatorEnum.UPDATED.value),
            processed_at=ioc_dict.get(IndicatorEnum.PROCESSED_AT.value),
            safelisted=ioc_dict.get(IndicatorEnum.SAFELISTED.value)
        )


    def serialize(self):
        serialized = super(PrioritizedIndicator, self).serialize()
        observable = serialized.get(OBSERVABLE).get("entity")
        attributes = [a.get("entity") for a in serialized.get(ATTRIBUTES)]
        serialized.update({OBSERVABLE: observable, ATTRIBUTES: attributes})
        return serialized
