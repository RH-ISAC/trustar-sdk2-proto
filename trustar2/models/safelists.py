from trustar2.base import typename
from trustar2.models.base import Base
from trustar2.trustar_enums import SafelistEnum



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
        entries = safelist_dict.get(SafelistEnum.ENTRIES.value)
        return cls(
            guid=safelist_dict.get(SafelistEnum.GUID.value),
            name=safelist_dict.get(SafelistEnum.NAME.value),
            company_guid=safelist_dict.get(SafelistEnum.COMPANY_GUID.value),
            excerpt=safelist_dict.get(SafelistEnum.EXCERPT.value),
            created_at=safelist_dict.get(SafelistEnum.CREATED_AT.value),
            updated_at=safelist_dict.get(SafelistEnum.UPDATED_AT.value),
            created_by=safelist_dict.get(SafelistEnum.CREATED_BY.value),
            updated_by=safelist_dict.get(SafelistEnum.UPDATED_BY.value),
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
            guid=entry_dict.get(SafelistEnum.GUID.value),
            entity=entry_dict.get(SafelistEnum.ENTITY.value),
            type=entry_dict.get(SafelistEnum.TYPE.value),
            created_by=entry_dict.get(SafelistEnum.CREATED_BY.value),
            created_at=entry_dict.get(SafelistEnum.CREATED_AT.value),
        )
