indicators_example_request = """{
   "queryTerm":"/Users/mknopf/code/test.sh",
   "enclaveGuids":[
      "3a93fab3-f87a-407a-9376-8eb3fae99b4e"
   ],
   "priorityScores":[
      3
   ],
   "types":[
      "SOFTWARE"
   ],
   "from":1596607968000,
   "to":1598308171000,
   "sortColumn":"PROCESSED_AT",
   "attributes":[
      {
         "type":"THREAT_ACTOR",
         "value":"BAD PANDA"
      }
   ],
   "cursor":"eyJwYWdlTnVtYmVyIjoxLCJwYWdlU2l6ZSI6Miwib2Zmc2V0Ijo0fQ=="
}"""

indicators_submission_example_request = """
{
  "title": "Report, complex test",
  "content": {
    "indicators": [
      {
        "observable": {
          "value": "verybadurl",
          "type": "URL"
        },
        "validFrom": 1604510497000,
        "validTo": 1607102497000,
        "maliciousScore": "BENIGN",
        "confidenceScore": "LOW",
        "attributes": [
          {
            "entity": {
              "value": "ActorName",
              "type": "THREAT_ACTOR"
            },
            "validFrom": 1604510497000,
            "validTo": 1607102497000,
            "confidenceScore": "LOW"
          },
          {
            "entity": {
              "value": "MalwareName",
              "type": "MALWARE"
            },
            "validFrom": 1604510497000,
            "validTo": 1607102497000,
            "confidenceScore": "MEDIUM"
          }
        ],
        "relatedObservables": [
          {
            "entity": {
              "value": "2.2.2.2",
              "type": "IP4"
            },
            "validFrom": 1604510497000,
            "validTo": 1607102497000,
            "confidenceScore": "LOW"
          },
          {
            "entity": {
              "value": "wwww.relatedUrl.com",
              "type": "URL"
            },
            "validFrom": 1604510497000,
            "validTo": 1607102497000,
            "confidenceScore": "HIGH"
          }
        ],
        "properties": {
          "propertyKey": "propertyValue"
        },
        "tags": [
          "importantTag",
          "anotherTag"
        ]
      }
    ]
  },
  "enclaveGuid": "c0f07a9f-76e4-48df-a0d4-c63ed2edccf0",
  "externalId": "external-1234",
  "externalUrl": "externalUrlValue",
  "timestamp": 1607102497000,
  "tags": ["random_tag"],
  "rawContent": "blob of text"
}
"""

non_structured_submission_example_request = """
{
  "title": "Report, complex test",
  "content": "MALICIOUS IP: 8.8.8.8",
  "enclaveGuid": "c0f07a9f-76e4-48df-a0d4-c63ed2edccf0",
  "externalId": "external-1234",
  "externalUrl": "externalUrlValue",
  "timestamp": 1607102497000,
  "tags": ["random_tag"]
}
"""


safelist_summaries = """
[
  {
    "guid": "test-library-guid-1",
    "name": "test-library-name-1",
    "companyGuid": "test-company-guid-1",
    "excerpt": "",
    "createdAt": 1618258235178,
    "updatedAt": 1618258235331,
    "createdBy": "test-user-1@trustar.co",
    "updatedBy": "test-user-1@trustar.co"
  },
  {
    "guid": "test-library-guid-2",
    "name": "test-library-name-2",
    "companyGuid": "test-company-guid-2",
    "excerpt": "",
    "createdAt": 1616791794869,
    "updatedAt": 1618288545872,
    "createdBy": "test-user-2@trustar.co",
    "updatedBy": "test-user-2@trustar.co"
  }
]
"""

safelist_details = """
{
  "guid": "test-library-guid-1",
  "name": "test-library-name-1",
  "companyGuid": "test-company-guid-1",
  "excerpt": "",
  "createdAt": 1618258235178,
  "updatedAt": 1618258235331,
  "createdBy": "test-user-1@trustar.co",
  "updatedBy": "test-user-1@trustar.co",
  "entries": [
      {
          "guid": "entry-guid-1",
          "entity": "good-email@test-domain.com",
          "type": "EMAIL_ADDRESS",
          "createdBy": "test-user-1@trustar.co",
          "createdAt": 1618288545871
      }
  ]
}
"""

entities_extraction = """
[
  {
      "entity": "8.8.8.8",
      "type": "IP4"
  },
  {
      "entity": "good-email@test-domain.com",
      "type": "EMAIL_ADDRESS"
  }
]
"""

enclaves = """
[
  {
      "name": "test_name_1",
      "templateName": "Private Enclave",
      "workflowSupported": false,
      "read": true,
      "create": true,
      "update": true,
      "id": "test-id-1",
      "type": "INTERNAL"
  },
  {
      "name": "test_name_2",
      "templateName": "Private Enclave",
      "workflowSupported": false,
      "read": true,
      "create": true,
      "update": true,
      "id": "test-id-2",
      "type": "INTERNAL"
  }
]
"""

serialized_workflow_config = """
{
  "type": "INDICATOR_PRIORITIZATION",
  "priorityScores": ["MEDIUM", "HIGH"],
  "observableTypes": ["URL", "IP4", "IP6", "SHA256"],
  "workflowSource": {
    "enclaveSourceConfig": [
      {
        "enclaveGuid": "test-enclave-id",
        "weight": 3
      },
      {
        "enclaveGuid": "test-enclave-id2",
        "weight": 3
      },
      {
        "enclaveGuid": "test-enclave-id3",
        "weight": 1
      },
      {
        "enclaveGuid": "test-enclave-id4",
        "weight": 5
      }
    ]
  },
  "workflowDestination": {
    "enclaveDestinationConfigs": [
      {
        "enclaveGuid": "test-enclave-id",
        "destinationType": "ENCLAVE"
      }
    ]
  }
}
"""

observables_search_example_request = """{
    "queryTerm": "query",
    "from":1596607968000,
    "to":1598308171000,
    "sortColumn": "FIRST_SEEN",
    "sortOrder": "ASC",
    "enclaveGuids": ["4bdc3f5b-3ed5-4d99-b20c-2d801866ef0b"],
    "types": ["MD5"]
}"""


prioritized_indicator = """
{
  "guid": "test-guid",
  "enclaveGuid": "test-enclave-guid",
  "workflowGuid": "test-workflow-guid",
  "observable": {
      "value": "2.2.2.2",
      "type": "IP4"
  },
  "priorityScore": "HIGH",
  "attributes": [
      {
          "value": "MalwareName",
          "type": "MALWARE"
      }
  ],
  "userTags": [],
  "submissionTags": [
      "malware"
  ],
  "scoreContexts": [
      {
        "enclaveGuid": "test-score-context-enclave-guid",
        "sourceName": "Test Source",
        "normalizedScore": 3,
        "weight": 3.0,
        "properties": {},
        "enclaveName": "Test Source"
      }
  ],
  "created": 1616176082000,
  "updated": 1624986245000,
  "processedAt": 1624990135728,
  "safelisted": false
}
"""


searched_observable = """
{
  "type": "IP4",
  "value": "2.2.2.2",
  "firstSeen": 1623273177255,
  "lastSeen": 1623701072520,
  "enclaveGuids": [
      "test-enclave-guid"
  ],
  "tags": ["test-tag"]
}
"""


searched_submission = """
{
  "guid": "test-guid",
  "enclaveGuid": "test-enclave-guid",
  "title": "Test Submission Title",
  "created": 1624980621003,
  "updated": 1624980621003,
  "tags": []
}
"""


enclave = """
{
  "name": "TestEnclave",
  "templateName": "Private Enclave",
  "workflowSupported": false,
  "read": true,
  "create": true,
  "update": true,
  "id": "test-id",
  "type": "INTERNAL"
}
"""


serialized_workflow = """
{
  "guid": "test-guid",
  "name": "Test Workflow",
  "created": 1616706603077,
  "updated": 1621540733425,
  "workflowConfig": {
    "type": "INDICATOR_PRIORITIZATION",
    "workflowSource": {
      "enclaveSourceConfig": [
        {
            "enclaveGuid": "test-source-id",
            "weight": 1
        }
      ]
    },
    "workflowDestination": {
      "enclaveDestinationConfigs": [
        {
            "enclaveGuid": "test-destination-id",
            "destinationType": "ENCLAVE"
        }
      ]
    },
    "observableTypes": [
      "IP4",
      "IP6",
      "EMAIL_ADDRESS",
      "URL",
      "MD5",
      "SHA256"
    ],
    "priorityScores": [
      "MEDIUM",
      "HIGH"
    ]
  },
  "safelistGuids": [
    "test-safelist-id"
  ]
}
"""
