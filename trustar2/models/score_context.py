from trustar2.base import typename
from trustar2.models.base import Base
from trustar2.trustar_enums import ScoreContextEnum


class ScoreContext(Base):

    def __init__(self, enclave_guid, source_name, normalized_score, weight, properties, enclave_name): 
        self.enclave_guid = enclave_guid
        self.source_name = source_name
        self.normalized_score = normalized_score
        self.weight = weight
        self.properties = properties
        self.enclave_name = enclave_name


    def __repr__(self):
        return "{}(name={}, weight={})".format(typename(self), self.source_name, self.weight)


    @classmethod
    def from_dict(cls, score_dict):
        return cls(
            enclave_guid=score_dict.get(ScoreContextEnum.ENCLAVE_GUID.value),
            source_name=score_dict.get(ScoreContextEnum.SOURCE_NAME.value),
            normalized_score=score_dict.get(ScoreContextEnum.NORMALIZED_SCORE.value),
            weight=score_dict.get(ScoreContextEnum.WEIGHT.value),
            properties=score_dict.get(ScoreContextEnum.PROPERTIES.value),
            enclave_name=score_dict.get(ScoreContextEnum.ENCLAVE_NAME.value)
        )
