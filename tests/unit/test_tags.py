from __future__ import unicode_literals

import pytest

from trustar2 import TagIndicator
from trustar2.trustar import TruStar


@pytest.fixture
def tag_indicator():
    return TagIndicator(
        TruStar(api_key="xxxx", api_secret="xxx", client_metatag="test_env")
    )


@pytest.mark.parametrize("added_tags,removed_tags", [(["important", "tag"], []),
                                                     ([], ["not_important", "tag"]),
                                                     (["important", "tag"], ["not_important"])])
def test_ok_alter_tags(tag_indicator, mocked_request, added_tags, removed_tags):
    expected_url = "https://api.trustar.co/api/2.0/indicators/cc12a5c6-e575-3879-8e41-2bf240cc6fce/alter-tags"
    mocked_request.post(url=expected_url, json={})

    request = (tag_indicator
               .set_added_tags(added_tags)
               .set_removed_tags(removed_tags)
               .set_enclave_id("3a93fab3-f87a-407a-9376-8eb3fae99b4e")
               .set_indicator_id("cc12a5c6-e575-3879-8e41-2bf240cc6fce")
               )
    request.alter_tags()

    params = request.payload_params.serialize()
    assert params.get("enclaveGuid") == "3a93fab3-f87a-407a-9376-8eb3fae99b4e"
    assert params.get("addedTags") == added_tags
    assert params.get("removedTags") == removed_tags


def test_alter_tag_incomplete(tag_indicator, mocked_request):
    expected_url = "https://api.trustar.co/api/2.0/indicators/cc12a5c6-e575-3879-8e41-2bf240cc6fce/alter-tags"
    mocked_request.post(url=expected_url, json={})

    # Missing added/removed tags
    with pytest.raises(AttributeError):
        q = (tag_indicator
             .set_enclave_ids("3a93fab3-f87a-407a-9376-8eb3fae99b4e")
             .set_indicator_id("cc12a5c6-e575-3879-8e41-2bf240cc6fce")
             .alter_tags()
             )

    # Missing enclave guid
    with pytest.raises(AttributeError):
        q = (tag_indicator
             .set_added_tags(["tag"])
             .set_indicator_id("cc12a5c6-e575-3879-8e41-2bf240cc6fce")
             .alter_tags()
             )

    # Missing indicator_id
    with pytest.raises(AttributeError):
        q = (tag_indicator
             .set_added_tags(["tag"])
             .set_enclave_ids("3a93fab3-f87a-407a-9376-8eb3fae99b4e")
             .alter_tags()
             )
