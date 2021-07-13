from trustar2.base import typename
from trustar2.models.base import Base

class SearchedObservable(Base):

    def __init__(self, type, value, first_seen, last_seen, enclave_guids, tags):
        self.type = type
        self.value = value
        self.first_seen = first_seen
        self.last_seen = last_seen
        self.enclave_guids = enclave_guids
        self.tags = tags


    def __repr__(self):
        return "{}(type={}, value={})".format(typename(self), self.type, self.value)


    @classmethod
    def from_dict(cls, obs_dict):
        return cls(
            type=obs_dict.get("type"),
            value=obs_dict.get("value"),
            first_seen=obs_dict.get("firstSeen"),
            last_seen=obs_dict.get("lastSeen"),
            enclave_guids=obs_dict.get("enclaveGuids"),
            tags=obs_dict.get("tags")
        )
