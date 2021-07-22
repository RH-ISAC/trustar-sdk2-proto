from trustar2.base import typename
from trustar2.models.base import Base


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
            enclave_guid=score_dict.get("enclaveGuid"),
            source_name=score_dict.get("sourceName"),
            normalized_score=score_dict.get("normalizedScore"),
            weight=score_dict.get("weight"),
            properties=score_dict.get("properties"),
            enclave_name=score_dict.get("enclaveName")
        )
