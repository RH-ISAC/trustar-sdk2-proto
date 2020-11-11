import json

from six import string_types

# package imports
from log import get_logger
from indicators import SearchIndicator

logger = get_logger(__name__)


class TruStar:

    # raise exception if any of these config keys are missing
    REQUIRED_KEYS = ('api_key', 'api_secret', 'client_metatag')

    # allow configs to use different key names for config values
    REMAPPED_KEYS = {
        'auth_endpoint': 'auth',
        'api_endpoint': 'base',
        'station_base_url': 'station',
        'user_api_key': 'api_key',
        'user_api_secret': 'api_secret'
    }

    def __init__(self, api_key, api_secret, client_metatag, **kwargs):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client_metatag = client_metatag

    @classmethod
    def config_from_file(cls, config_file_path, config_role):
        with open(config_file_path, "r") as f:
            config_file = json.load(f)

        config = config_file.get(config_role)
        if not config:
            raise AttributeError("{} role was not found in {} file".format(
                config_role, config_file_path
            ))

        trustar = cls(**config)
        return trustar


    def indicators(self):
        # TODO add condig
        return SearchIndicator(self)


# trustar = TruStar.config_from_file("trustar_config.json", "station")

# print trustar.api_key
# print trustar.api_secret
# print trustar.client_metatag


# print("Hello")
# indicators = TruStar(auth="https://staging.trustar.co/oauth/token",
#                      api_key="",
#                      secret="").indicators().set_query_term("181.").query()
# for n in indicators:
#     print(n)
