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

    def __init__(self, auth, api_key, secret):
        self.auth = auth
        self.api_key = api_key
        self.secret = secret

    @staticmethod
    def config_from_file(config_file_path, config_role):
        raise NotImplemented

    def indicators(self):
        # TODO add condig
        return SearchIndicator(self)


print("Hello")
indicators = TruStar(auth="https://staging.trustar.co/oauth/token",
                     api_key="",
                     secret="").indicators().set_query_term("181.").query()
for n in indicators:
    print(n)
