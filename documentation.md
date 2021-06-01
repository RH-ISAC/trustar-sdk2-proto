# Usage Examples

### Overview

 - [Submissions](#submissions)
 - [Search Indicators](#search-indicators)
 - [Safelists](#safelists)
 - [Data Model](#data-model)
 - [Workflows](#worklows-management)

# Config

To use the SDK you will need a json config file. 

You can find a template of `trustar_config.json` [here](trustar_config.json)

# Submissions
## Create / Update submissions in TruSTAR

The `upsert` method will create a new submission in TruSTAR if the external id does not exist, or will update the existing one if it can find it.

## Create

```python
from trustar2 import TruStar
from trustar2.models import Indicator, Entity

indicator = Indicator("IP4", "1.2.3.4")

indicator.set_related_observables(Entity.observable("IP4", "8.8.8.8").set_confidence_score("MEDIUM"))
indicator.set_attributes(Entity.attribute("MALWARE", "SOME MALWARE").set_confidence_score("MEDIUM"))
indicator.set_malicious_score("HIGH")
indicator.set_tags(["<some-tag-1>","<some-tag-2>"])


TruStar.config_from_file("trustar_config.json", "station")\
    .submission()\
    .set_title("<your-title>")\
    .set_content_indicators([indicator])\
    .set_external_id("12345")\
    .set_enclave_id("<your-enclave-id>")\
    .upsert()
```


## Update 

```python
from trustar2 import TruStar
from trustar2.models import Indicator, Entity

indicator = Indicator("IP4", "0.0.0.0")

TruStar.config_from_file("trustar_config.json", "station")\
    .submission()\
    .set_title("<NEW-title>")\ #updating title
    .set_content_indicators([indicator])\ #updating indicator
    .set_external_id("12345")\
    .set_enclave_id("<your-enclave-id>")\
    .set_id_type_as_external(True)\
    .upsert()
```


## Get submission from TruSTAR

```python
from trustar2 import TruStar

TruStar.config_from_file("trustar_config.json", "station")\
    .submission()\
    .set_external_id("12345")\
    .set_enclave_id("<your-enclave-id>")\
    .set_id_type_as_external(True)\
    .set_include_content(True)\
    .get()
```

## Delete submissions from TruSTAR

```python
from trustar2 import TruStar

TruStar.config_from_file("trustar_config.json", "station")\
    .submission()\
    .set_external_id("12345")\
    .set_enclave_id("<your-enclave-id>")\
    .set_id_type_as_external(True)\
    .set_include_content(True)\
    .delete()
```

# Search Indicators
```python
from trustar2 import TruStar
response = TruStar.config_from_file("trustar_config.json", "station")\
        .indicators()\
        .set_enclave_ids(["<your-enclave-id>"])\
        .search()

    for page in response:
        pprint(page.json().get("items"))
```

## Using SDK without the fluent interface

You can use the SDK without having to call to the `submission` and `indicators` methods from the `TruStar` class. And you can work with your config and submission / indicator search, in a decoupled way.

```python
from trustar2 import TruStar, Submission

trustar_config = TruStar.config_from_file("trustar_config.json", "station")
submission = Submission()

# Lines of code

submission.set_id("your-id")
submissions.set_include_content(True) 

# More lines of code

submission.set_trustar_config(trustar_config)
submission.get()
```


# Safelists

## Retrieve Safelist Summaries

```python
ts = TruStar.config_from_file("trustar_config.json", "station")
response = ts.safelist().get_safelist_libraries()
```

## Retrieve Safelist Details 

```python
ts = TruStar.config_from_file("trustar_config.json", "station")
response = ts.safelist() \
    .set_library_guid("<library-guid>") \
    .get_safelist_details()
```


## Creating entries in a safelist

```python
ts = TruStar.config_from_file("trustar_config.json", "station")
response = ts.safelist() \
    .set_library_guid("<library-guid>") \
    .set_safelist_entries([{"entity": "8.8.8.8", "type": "IP4"}]) \
    .create_entries() 
```


## Creating a new empty safelist

```python
ts = TruStar.config_from_file("trustar_config.json", "station")
response = ts.safelist() \
    .set_library_name("<NAME>") \
    .create_safelist() 
```


## Deleting an entry from a safelist

```python
ts = TruStar.config_from_file("trustar_config.json", "station")
response = ts.safelist().set_library_guid("<library-guid>").delete_entry("<entry-guid>")
```


## Deleting a safelist 

```python
ts = TruStar.config_from_file("trustar_config.json", "station")
response = ts.safelist().set_library_guid("<library-guid>").delete_safelist()
```


## Extracting entities

```python
ts = TruStar.config_from_file("trustar_config.json", "station")
text_blob = "8.8.8.8 - example@domain.com" # This can be any unstructured text containing multiple observables
response = ts.safelist().set_text_to_be_extracted(text_blob).extract_terms()
```

# Workflows Management

## Creating a new workflow

```python
wsc1 = WorkflowSourceConfig("<enclave-id-1>", 5)
wsc2 = WorkflowSourceConfig("<enclave-id-2>", 3)
wsc3 = WorkflowSourceConfig("<enclave-id-3>", 4)

wc = WorkflowConfig()
wc.set_source_configs([wsc1, wsc2, wsc3])
wc.set_destination_configs(("<destination-enclave-id>", "ENCLAVE"))
wc.set_priority_scores(["MEDIUM", "HIGH"])
wc.set_observable_types(["URL", "IP4", "IP6", "SHA256"])

response = (TruStar.config_from_file("trustar_config.json", "station")
                .workflows()
                .set_name("<WORKFLOW-TITLE>")
                .set_workflow_config(wc)
                .set_safelist_ids(["<safelist-guid>"])
                .create()
)
```

## Updating a workflow

```python
wsc1 = WorkflowSourceConfig("<enclave-id-1>", 5)
wsc2 = WorkflowSourceConfig("<enclave-id-2>", 3)
wsc3 = WorkflowSourceConfig("<enclave-id-3>", 4)

wc = WorkflowConfig()
wc.set_source_configs([wsc1, wsc2, wsc3])
wc.set_destination_configs(("<destination-enclave-id>", "ENCLAVE"))
wc.set_priority_scores(["HIGH"]) # Updating Scores
wc.set_observable_types(["IP4", "IP6", "SHA256", "SHA1"]) # Updating Types

response = (TruStar.config_from_file("trustar_config.json", "station")
                .workflows()
                .set_name("<WORKFLOW-TITLE>")
                .set_workflow_config(wc)
                .set_safelist_ids(["<safelist-guid>"])
                .set_workflow_id("<workflow-id>")
                .update()
)
```

## Getting all workflows

```python
response = (TruStar.config_from_file("trustar_config.json", "station")
                .workflows()
                .get()
)
```

## Getting a workflow by ID

```python
response = (TruStar.config_from_file("trustar_config.json", "station")
                .workflows()
                .set_workflow_id("<workflow-id>")
                .get()
)
```


## Deleting a workflow

```python
response = (TruStar.config_from_file("trustar_config.json", "station")
                .workflows()
                .set_workflow_id("<workflow-id>")
                .delete())
```



# Data Model

## Submission

| Setter | Param Type | Functionality | Mandatory? |
| :----------------: | :----: | :----: | :----: |
| `.set_title` | String | Title of the submission | Yes on Creation, optional while updating |
| `.set_content_indicators`| List of [Indicator](#indicator) objects| Indicators to be included in the submission|Yes on Creation, optional while updating|
| `.set_enclave_id` | String | Enclave where the submission will be created/deleted/fetched | Yes on creation. While updating / fetching / deleting, it's mandatory IF id type was marked as external|
| `.set_external_url` | String | url for an external report| No. Optional always |
| `.set_timestamp` | Int (unix timestamp) or python Date | Submission's timestamp| No. Optional always |
| `.set_include_content` | Boolean | Indicates if submission body should be returned while fetching submissions| No. Optional while fetching submissions|
| `.set_id` | String | Submission Guid | Yes while updating / deleting / fetching submissions. IF id type was marked as external you can choose between using this method or `set_extetnal_id`|
| `.set_external_id` | String | Submission external ID, should be unique on each enclave | No. Optional always. |
| `.set_id_type_as_external` | Boolean | Indicates if the ID used to fetch / delete a submission is external or not | No. Optional always. |
| `.set_raw_content` | String | Unstructured text blob | No. Optional always. |
| `.set_tags` | List of String | Tags to be included on the report | No. Optional always. |
| `.set_submission_version` | Integer | Submission version, if creating should be 0 | Yes when creating or updating submissions|

## Search Indicator

| Setter | Param Type | 
| :----------------: | :----: |
|`.set_query_term`| String |
|`.set_from`|Int (unix timestamp) or python Date|
|`.set_to`|Int (unix timestamp) or python Date|
|`.set_priority_scores`| List of Integers between -1 and 3|
|`.set_sort_column`| String / [Enum](trustar2/trustar_enums.py#L11)|
|`.set_enclave_ids`| Single or List of Strings|
|`.set_observable_types`| List of Strings or [Enums](trustar2/trustar_enums.py#L18)|
|`.set_attributes`| List of Strings or [Enums](trustar2/trustar_enums.py#L35)|
|`.set_related_observables`|List of Strings or [Enums](trustar2/trustar_enums.py#L18)|

Only mandatory setter is `.set_enclave_ids` .

Other setters are not mandatory, but if you want to filter the returned IOCs, you need call the right method.

## Indicator

| Attribute / Setter | Param Type |
| :----------------: | :----: |
| Observable Type | String  / [Enum](trustar2/trustar_enums.py#L18)|
| Observable Value | String |
| `.set_related_observables` | List of / or single [Observable](#observable) entity |
| `.set_attributes`| List of / or single [Attribute](#attribute) entity|
| `.set_malicious_score` | String  ("BENIGN", "LOW", "MEDIUM", "HIGH")|
| `.set_confidence_score` | String  ("LOW", "MEDIUM", "HIGH")|
| `.set_valid_from` | Int (unix timestamp) or python Date |
| `.set_valid_to` | Int (unix timestamp) or python Date  |
| `.set_tags` | List of / or single String |

## Observable 

| Attribute / Setter | Param Type |
| :----------------: | :----: |
| Observable Type | String  / [Enum](trustar2/trustar_enums.py#L18)|
| Observable Value | String |
| `.set_confidence_score` | String ("LOW", "MEDIUM", "HIGH") |
| `.set_valid_from` | Int (unix timestamp) or python Date |
| `.set_valid_to` | Int (unix timestamp) or python Date |


## WorkflowConfig 

| Attribute / Setter | Param Type |
| :----------------: | :----: |
| `.set_source_configs` | The parameter can be a single element or a list of one of the following types: [**WorkflowSourceConfig**](#workflowsourceconfig) / **tuple** - `(enclave_guid, weight)` / **dict**  - `{"enclave_guid": enclave_guid, "weight": weight}`|
| `.set_destination_configs` | The parameter can be a single element or a list of one of the following types: [**WorkflowDestinationConfig**](#workflowdestinationconfig) / **tuple** - `(enclave_guid, destinationType)` / **dict**  - `{"enclave_guid": enclave_guid, "destination_type": destination_type}` |
| `.set_priority_scores` | List of strings ("BENIGN", "LOW", "MEDIUM", "HIGH") |
| `.set_observable_types` | List of strings or [Enums](trustar2/trustar_enums.py#L18)|



## WorkflowSourceConfig 

| Attribute / Setter | Param Type |
| :----------------: | :----: |
| `enclave_guid` | String |
| `weight` | int |


## WorkflowDestinationConfig 

| Attribute / Setter | Param Type |
| :----------------: | :----: |
| `enclave_guid` | String |
| `destination_type` | String / [Enum](trustar2/trustar_enums.py#L64) |


## Attribute 

| Attribute / Setter | Param Type |
| :----------------: | :----: |
| Attribute Type | String  / [Enum](trustar2/trustar_enums.py#L35)|
| Attribute Value | String |
| `.set_confidence_score` | String ("LOW", "MEDIUM", "HIGH") |
| `.set_valid_from` | Int (unix timestamp) or python Date |
| `.set_valid_to` | Int (unix timestamp) or python Date |

[Valid observable / attribute types](trustar2/trustar_enums.py#L18): 

Attribute: 
- THREAT_ACTOR
- MALWARE
- CARO_MALWARE
- CVE

Observables
- IP4
- IP6
- CIDR_BLOCK
- EMAIL_ADDRESS
- URL
- MD5
- SHA1
- SHA256
- REGISTRY_KEY
- SOFTWARE
- BITCOIN_ADDRESS
- PHONE_NUMBER
- X_ID
