from trustar2.base import typename
from trustar2.models.base import Base

class SearchedSubmission(Base):

    def __init__(self, guid, enclave_guid, title, created, updated, tags):
        self.guid = guid
        self.enclave_guid = enclave_guid
        self.title = title
        self.created = created
        self.updated = updated
        self.tags = tags


    def __repr__(self):
        return "{}(title={})".format(typename(self), self.title)


    @classmethod
    def from_dict(cls, sub_dict):
        return cls(
            guid=sub_dict.get("guid"),
            enclave_guid=sub_dict.get("enclaveGuid"),
            title = sub_dict.get("title"),
            created=sub_dict.get("created"),
            updated=sub_dict.get("updated"),
            tags=sub_dict.get("tags")
        )
