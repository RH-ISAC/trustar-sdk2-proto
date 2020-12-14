from enum import Enum, EnumMeta
from six import with_metaclass


class TSEnum(Enum):

    @classmethod
    def members(cls):
        return (m.value for m in cls)


class SortColumns(TSEnum):
    
    UPDATED = "UPDATED"
    CREATED = "CREATED"
    PROCESSED_AT = "PROCESSED_AT"    


class MetaObservable(EnumMeta):

    def __str__(cls):
        return "observable"


class MetaAttribute(EnumMeta):

    def __str__(cls):
        return "attribute"


class ObservableTypes(with_metaclass(MetaObservable, TSEnum)):
    IP4 = "IP4"
    IP6 = "IP6"
    URL = "URL"
    SHA1 = "SHA1"
    SHA256 = "SHA256"
    EMAIL_ADDRESS = "EMAIL_ADDRESS"
    PHONE_NUMBER = "PHONE_NUMBER"
    MD5 = "MD5"
    BITCOIN = "BITCOIN"
    XID = "XID"
    REGISTRY_KEY = "REGISTRY_KEY"
    SOFTWARE = "SOFTWARE"
    CIDR_BLOCK = "CIDR_BLOCK"


class AttributeTypes(with_metaclass(MetaAttribute, TSEnum)):
    MALWARE = "MALWARE"
    CORA_MALWARE = "CORA_MALWARE"
    THREAT_ACTOR = "THREAT_ACTOR"
    CVE = "CVE"
    MITRE_TACTIC = "MITRE_TACTIC"
