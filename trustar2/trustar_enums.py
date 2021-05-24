from enum import Enum


class TSEnum(Enum):

    @classmethod
    def members(cls):
        return (m.value for m in cls)


class SortColumns(TSEnum):
    
    CREATED = "CREATED"
    PROCESSED_AT = "PROCESSED_AT"
    UPDATED = "UPDATED"


class SortOrder(TSEnum):
    ASC = "ASC"
    DESC = "DESC"


class ObservableTypes(TSEnum):

    BITCOIN_ADDRESS = "BITCOIN_ADDRESS"
    CIDR_BLOCK = "CIDR_BLOCK"
    EMAIL_ADDRESS = "EMAIL_ADDRESS"
    IP4 = "IP4"
    IP6 = "IP6"
    MD5 = "MD5"
    PHONE_NUMBER = "PHONE_NUMBER"
    REGISTRY_KEY = "REGISTRY_KEY"
    SHA1 = "SHA1"
    SHA256 = "SHA256"
    SOFTWARE = "SOFTWARE"
    URL = "URL"
    X_ID = "X_ID"


class AttributeTypes(TSEnum):
    
    CORA_MALWARE = "CORA_MALWARE"
    CVE = "CVE"
    MALWARE = "MALWARE"
    MITRE_TACTIC = "MITRE_TACTIC"
    THREAT_ACTOR = "THREAT_ACTOR"


class TruStarUrls(TSEnum):

    API = "https://api.trustar.co/api/2.0"
    AUTH_TOKEN = "https://api.trustar.co/oauth/token"
    STATION = "https://station.trustar.co"


class MaxValues(TSEnum):

    TAGS = 20
    RELATED_OBSERVABLES = 50
    ATTRIBUTES = 50
    INDICATORS = 2000
