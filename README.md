# TruSTAR SDK 2

# Documentation
## Create new submissions in TruSTAR

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
    .set_submission_version(0)\
    .create()
```
You can find a template of `trustar_config.json` [here](trustar_config.json)

## Update submission in TruSTAR

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
    .set_submission_version(1)\ # new submissions version
    .update()
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

## Search Indicators
```python
from trustar2 import TruStar
response = TruStar.config_from_file("trustar_config.json", "station")\
        .indicators()\
        .set_enclave_ids(["<your-enclave-id>"])\
        .search()

    for page in response:
        pprint(page.json().get("items"))
```

## Submission

| Setter | Param Type | Functionality | Mandatory? |
| :----------------: | :----: | :----: | :----: |
| `.set_title` | String | Title of the submission | Yes on Creation, optional while updating |
| `.set_content_indicators`| List of [Indicator](indicator) objects| Indicators to be included in the submission|Yes on Creation, optional while updating|
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
|`.set_sort_column`| String / Enum |
|`.set_enclave_ids`| Single or List of Strings|
|`.set_observable_types`| List of Strings or Enums|
|`.set_attributes`| List of Strings or Enums |
|`.set_related_observables`|List of Strings or Enums|


## Indicator

| Attribute / Setter | Param Type |
| :----------------: | :----: |
| Observable Type | String  / Enum|
| Observable Value | String |
| `.set_related_observables` | List of / or single Observable entity |
| `.set_attributes`| List of / or single Attribute entity|
| `.set_malicious_score` | String  ("BENIGN", "LOW", "MEDIUM", "HIGH")|
| `.set_confidence_score` | String  ("LOW", "MEDIUM", "HIGH")|
| `.set_valid_from` | Int (unix timestamp) or python Date |
| `.set_valid_to` | Int (unix timestamp) or python Date  |
| `.set_tags` | List of / or single String |

## Observable 

| Attribute / Setter | Param Type |
| :----------------: | :----: |
| Observable Type | String  / Enum|
| Observable Value | String |
| `.set_confidence_score` | String ("LOW", "MEDIUM", "HIGH") |
| `.set_valid_from` | Int (unix timestamp) or python Date |
| `.set_valid_to` | Int (unix timestamp) or python Date |

## Attribute 

| Attribute / Setter | Param Type |
| :----------------: | :----: |
| Attribute Type | String  / Enum|
| Attribute Value | String |
| `.set_confidence_score` | String ("LOW", "MEDIUM", "HIGH") |
| `.set_valid_from` | Int (unix timestamp) or python Date |
| `.set_valid_to` | Int (unix timestamp) or python Date |

[Valid observable / attribute types](.trustar2/trustar_enums): 

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

# Project development setup

This repository is built using tox to test the code with diferrent python versions. If you want to set up your development environment follow the instructions.

1. If you don't have tox installed in your sysem

`pip install tox`

2.

`tox --devenv <virtualenv_name> -e <python_environment>`

Where virtualenv_name is the name you choose for your virtual environment and python_environment is one of the supported python version `py27` or `py37`.

### Example:

`tox --devenv .venv-py37 -e py37`

3.

Activate your virtual environment:

`source .venv-py37/bin/activate`

# Running tests

If you want to test all available environments:, just do:

`tox` in project's root

If you want to run a specific environment:

`tox -e py27` or `tox -e py37`

# Releasing a new version

To publish a new version in PyPI you should use the `release.sh` script that is in the root of the project. Suppose you want to release v0.0.1, you should do:

```
bash release.sh v0.0.1
```

Obviously, in order to make a release, you must have permissions to do so and you must have your PyPI creds available for Twine.
