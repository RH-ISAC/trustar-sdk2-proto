import json

from six import string_types

# package imports
from log import get_logger
from indicators import SearchIndicator

from version import __version__, __api_version__

logger = get_logger(__name__)


class TruStar:

    DEFAULTS = {
        'auth_endpoint': 'https://staging.trustar.co/oauth/token',
        'api_endpoint': 'https://staging.trustar.co/api/2.0',
        'station': "https://staging.trustar.co",
        'client_type': 'PYTHON_SDK',
        'client_version': __version__,
        'verify': True,
        'retry': True,
        'max_wait_time': 60,
        'http_proxy': None,
        'https_proxy': None
    }

    def __init__(self, api_key, api_secret, client_metatag, **kwargs):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client_metatag = client_metatag
        self.request_details = self.DEFAULTS.copy()
        self.request_details.update(kwargs)


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


indicators = TruStar.config_from_file("trustar_config.json",
                                      "staging").indicators().query()
import json
for n in indicators:
    print(json.dumps(n.json()))

