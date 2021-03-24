indicators_example_request = """{
   "queryTerm":"/Users/mknopf/code/test.sh",
   "enclaveIds":[
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
