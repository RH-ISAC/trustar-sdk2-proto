from trustar2.base import typename
from trustar2.models.base import Base
from trustar2.models.indicator import Indicator
from trustar2.trustar_enums import SubmissionEnum


class SubmissionDetails(Base):

    def __init__(self, id, title, content, enclave_guid, external_id, external_url, 
                 timestamp, created, updated, tags, submission_version):

        self.id = id
        self.title = title
        self.content = content
        self.enclave_guid = enclave_guid
        self.external_id = external_id
        self.external_url = external_url
        self.timestamp = timestamp
        self.created = created
        self.updated = updated
        self.tags = tags
        self.submission_version = submission_version


    def __repr__(self):
        return "{}(title={})".format(typename(self), self.title)



class StructuredSubmissionDetails(SubmissionDetails):

    def __init__(self, id, title, content, enclave_guid, external_id, external_url, 
                 timestamp, created, updated, tags, submission_version, raw_content):

        content_indicators = [Indicator.from_dict(i) for i in content.get("indicators")]
        content.update({"indicators": content_indicators})
        super(StructuredSubmissionDetails, self).__init__(
            id, title, content, enclave_guid, 
            external_id, external_url, timestamp, 
            created, updated, tags, submission_version
        )
        self.raw_content = raw_content


    @classmethod
    def from_dict(cls, sub_dict):
        return cls(
            id=sub_dict.get(SubmissionEnum.ID.value),
            title=sub_dict.get(SubmissionEnum.TITLE.value),
            content=sub_dict.get(SubmissionEnum.CONTENT.value),
            enclave_guid=sub_dict.get(SubmissionEnum.ENCLAVE_GUID.value),
            external_id=sub_dict.get(SubmissionEnum.EXTERNAL_ID.value),
            external_url=sub_dict.get(SubmissionEnum.EXTERNAL_URL.value),
            timestamp=sub_dict.get(SubmissionEnum.TIMESTAMP.value),
            created=sub_dict.get(SubmissionEnum.CREATED.value),
            updated=sub_dict.get(SubmissionEnum.UPDATED.value),
            tags=sub_dict.get(SubmissionEnum.TAGS.value),
            submission_version=sub_dict.get(SubmissionEnum.SUBMISSION_VERSION.value),
            raw_content=sub_dict.get(SubmissionEnum.RAW_CONTENT.value)
        )


    def serialize(self):
        serialized = super(StructuredSubmissionDetails, self).serialize()
        content_indicators = [i.serialize() for i in serialized.get(SubmissionEnum.CONTENT.value).get("indicators")]
        serialized.update({SubmissionEnum.CONTENT.value: {"indicators": content_indicators}})
        return serialized



class UnstructuredSubmissionDetails(SubmissionDetails):

    def __init__(self, id, title, content, enclave_guid, external_id, external_url, 
                 timestamp, created, updated, tags, submission_version):

        super(UnstructuredSubmissionDetails, self).__init__(
            id, title, content, enclave_guid, 
            external_id, external_url, timestamp, 
            created, updated, tags, submission_version
        )


    @classmethod
    def from_dict(cls, sub_dict):
        return cls(
            id=sub_dict.get(SubmissionEnum.ID.value),
            title=sub_dict.get(SubmissionEnum.TITLE.value),
            content=sub_dict.get(SubmissionEnum.CONTENT.value),
            enclave_guid=sub_dict.get(SubmissionEnum.ENCLAVE_GUID.value),
            external_id=sub_dict.get(SubmissionEnum.EXTERNAL_ID.value),
            external_url=sub_dict.get(SubmissionEnum.EXTERNAL_URL.value),
            timestamp=sub_dict.get(SubmissionEnum.TIMESTAMP.value),
            created=sub_dict.get(SubmissionEnum.CREATED.value),
            updated=sub_dict.get(SubmissionEnum.UPDATED.value),
            tags=sub_dict.get(SubmissionEnum.TAGS.value),
            submission_version=sub_dict.get(SubmissionEnum.SUBMISSION_VERSION.value)
        )
