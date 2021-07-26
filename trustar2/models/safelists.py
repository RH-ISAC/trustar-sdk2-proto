from trustar2.base import typename
from trustar2.models.base import Base



class SafelistLibrary(Base):


    def __init__(self, guid, name, company_guid, excerpt, created_at,
                 updated_at, created_by, updated_by, entries):
        self.guid = guid
        self.name = name
        self.company_guid = company_guid
        self.excerpt = excerpt
        self.created_at = created_at
        self.updated_at = updated_at
        self.created_by = created_by
        self.updated_by = updated_by
        self.entries = entries

    
    def __repr__(self): 
        return "{}(name={}, guid={})".format(typename(self), self.name, self.guid)


    @classmethod
    def from_dict(cls, safelist_dict): 
        entries = safelist_dict.get("entries")
        return cls(
            guid=safelist_dict.get("guid"),
            name=safelist_dict.get("name"),
            company_guid=safelist_dict.get("companyGuid"),
            excerpt=safelist_dict.get("excerpt"),
            created_at=safelist_dict.get("createdAt"),
            updated_at=safelist_dict.get("updatedAt"),
            created_by=safelist_dict.get("createdBy"),
            updated_by=safelist_dict.get("updatedBy"),
            entries=[SafelistEntry.from_dict(e) for e in entries] if entries is not None else None,
        )



class SafelistEntry(Base):


    def __init__(self, guid, entity, type, created_by, created_at):
        self.guid = guid
        self.entity = entity
        self.type = type
        self.created_by = created_by
        self.created_at = created_at


    def __repr__(self): 
        return "{}(entity={}, type={})".format(typename(self), self.entity, self.type)


    @classmethod
    def from_dict(cls, entry_dict): 
        return cls(
            guid=entry_dict.get("guid"),
            entity=entry_dict.get("entity"),
            type=entry_dict.get("type"),
            created_by=entry_dict.get("createdBy"),
            created_at=entry_dict.get("createdAt"),
        )
