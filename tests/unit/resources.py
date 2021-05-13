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

submission_example_request = """
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
