from trustar2.models.indicator import Indicator


class SubmissionDetails(object):


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



class StructuredSubmissionDetails(SubmissionDetails):


    def __init__(self, id, title, content, enclave_guid, external_id, external_url, 
                 timestamp, created, updated, tags, submission_version, raw_content):

        content_indicators = [Indicator.from_dict(i) for i in content.get("indicators")]
        content.updade({"indicators": content_indicators})
        super(StructuredSubmissionDetails, self).__init__(
            id, title, content, enclave_guid, 
            external_id, external_url, timestamp, 
            created, updated, tags, submission_version
        )
        self.raw_content = raw_content


    @classmethod
    def from_dict(cls, sub_dict):
        return cls(
            id=sub_dict.get("id"),
            title=sub_dict.get("title"),
            content=sub_dict.get("content"),
            enclave_guid=sub_dict.get("enclaveGuid"),
            external_id=sub_dict.get("externalId"),
            external_url=sub_dict.get("externalUrl"),
            timestamp=sub_dict.get("timestamp"),
            created=sub_dict.get("created"),
            updated=sub_dict.get("updated"),
            tags=sub_dict.get("tags"),
            submission_version=sub_dict.get("submissionVersion"),
            raw_content=sub_dict.get("rawContent")
        )



class UnstructuredSubmissionDetails(SubmissionDetails):


    def __init__(self, id, title, content, enclave_guid, external_id, external_url, 
                 timestamp, created, updated, tags, submission_version):

        super(StructuredSubmissionDetails, self).__init__(
            id, title, content, enclave_guid, 
            external_id, external_url, timestamp, 
            created, updated, tags, submission_version
        )


    @classmethod
    def from_dict(cls, sub_dict):
        return cls(
            id=sub_dict.get("id"),
            title=sub_dict.get("title"),
            content=sub_dict.get("content"),
            enclave_guid=sub_dict.get("enclaveGuid"),
            external_id=sub_dict.get("externalId"),
            external_url=sub_dict.get("externalUrl"),
            timestamp=sub_dict.get("timestamp"),
            created=sub_dict.get("created"),
            updated=sub_dict.get("updated"),
            tags=sub_dict.get("tags"),
            submission_version=sub_dict.get("submissionVersion")
        )
