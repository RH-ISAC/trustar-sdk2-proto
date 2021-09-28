from __future__ import unicode_literals

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
    DOMAIN = 'DOMAIN'


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


class WorkflowDestinations(TSEnum):

    QRADAR = "QRADAR"
    ENCLAVE = "ENCLAVE"
    SPLUNK = "SPLUNK"
    SPLUNK_ES = "SPLUNK_ES"
    UNKNOWN = "UNKNOWN"


class ID_Types(TSEnum):

    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"
    UNRECOGNIZED = "UNRECOGNIZED"


class ObservableSortColumns(TSEnum):

    FIRST_SEEN = "FIRST_SEEN"
    LAST_SEEN = "LAST_SEEN"


class MaliciousScore(TSEnum):
    BENIGN = "BENIGN"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ConfidenceScore(TSEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class SubmissionEnum(TSEnum):
    ID = "id"
    TITLE = "title"
    CONTENT = "content"
    ENCLAVE_GUID = "enclaveGuid"
    EXTERNAL_ID = "externalId"
    EXTERNAL_URL = "externalUrl"
    TAGS = "tags"
    ID_TYPE = "idType"
    INCLUDE_CONTENT = "includeContent"
    TIMESTAMP = "timestamp"
    RAW_CONTENT = "rawContent"
    SUBMISSION_VERSION = "submissionVersion"
    GUID = "guid"
    CREATED = "created"
    UPDATED = "updated"


class ObservablesEnum(TSEnum):
    TYPE = "type"
    TYPES = "types"
    VALUE = "value"
    FIRST_SEEN = "firstSeen"
    LAST_SEEN = "lastSeen"
    ENCLAVE_GUIDS = "enclaveGuids"
    TAGS = "tags"
    OBSERVABLE_VALUE = "observableValue"
    SUBMISSION_ID = "submissionId"
    ID_TYPE = "idType"


class SafelistEnum(TSEnum):
    ENTRIES = "entries"
    NAME = "name"
    TEXT = "text"
    GUID = "guid"
    COMPANY_GUID = "companyGuid"
    EXCERPT = "excerpt"
    CREATED_AT = "createdAt"
    CREATED_BY = "createdBy"
    UPDATED_AT = "updatedAt"
    UPDATED_BY = "updatedBy"
    TYPE = "type"
    ENTITY = "entity"


class SearchEnum(TSEnum):
    QUERY_TERM = "queryTerm"
    FROM = "from"
    TO = "to"
    ENCLAVE_GUIDS = "enclaveGuids"
    SORT_COLUMN = "sortColumn"
    SORT_ORDER = "sortOrder"
    PAGE_SIZE = "pageSize"
    INCLUDED_TAGS = "includedTags"
    EXCLUDED_TAGS = "excludedTags"


class TagsEnum(TSEnum):
    ADDED_TAGS = "addedTags"
    REMOVED_TAGS = "removedTags"
    ENCLAVE_ID = "enclaveId" # Used for submissions
    ENCLAVE_GUID = "enclaveGuid" # Used almost in every other place


class IndicatorEnum(TSEnum):
    TYPES = "types"
    ATTRIBUTES = "attributes"
    RELATED_OBSERVABLES = "relatedObservables"
    INCLUDE_SAFELISTED = "includeSafelisted"
    GUID = "guid"
    ENCLAVE_GUID = "enclaveGuid"
    WORKFLOW_GUID = "workflowGuid"
    PRIORITY_SCORE = "priorityScore"
    PRIORITY_SCORES = "priorityScores"
    USER_TAGS = "userTags"
    SUBMISSION_TAGS = "submissionTags"
    CREATED = "created"
    UPDATED = "updated"
    PROCESSED_AT = "processedAt"
    SAFELISTED = "safelisted"
    SCORE_CONTEXTS = "scoreContexts"
    OBSERVABLE = "observable"
    TYPE = "type"
    VALUE = "value"
    TAGS = "tags"


class WorkflowEnum(TSEnum):
    NAME = "name"
    TYPE = "type"
    CREATED_FROM = "createdFrom"
    CREATED_TO = "createdTo"
    UPDATED_FROM = "updatedFrom"
    UPDATED_TO = "updatedTo"
    WORKFLOW_CONFIG = "workflowConfig"
    SAFELIST_GUIDS = "safelistGuids"
    ENCLAVE_GUID = "enclaveGuid"
    DESTINATION_TYPE = "destinationType"
    WEIGHT = "weight"
    WORKFLOW_SOURCE = "workflowSource"
    WORKFLOW_DEST = "workflowDestination"
    ENCLAVE_SOURCE_CONFIG = "enclaveSourceConfig"
    ENCLAVE_DEST_CONFIG = "enclaveDestinationConfigs"
    OBSERVABLE_TYPES = "observableTypes"
    PRIORITY_SCORES = "priorityScores"


class EnclaveEnum(TSEnum):
    NAME = "name"
    TEMPLATE_NAME = "templateName"
    WORKFLOW_SUPPORTED = "workflowSupported"
    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    ID = "id"
    TYPE = "type"


class ScoreContextEnum(TSEnum):
    ENCLAVE_GUID = "enclaveGuid"
    SOURCE_NAME = "sourceName"
    NORMALIZED_SCORE = "normalizedScore"
    WEIGHT = "weight"
    PROPERTIES = "properties"
    ENCLAVE_NAME = "enclaveName"
