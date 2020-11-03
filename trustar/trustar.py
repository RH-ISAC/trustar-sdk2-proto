from six import string_types

# package imports
from .log import get_logger
from .api_client import SearchIndicator

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

    def __init__(self, config):
        # remap config keys names
        for k, v in self.REMAPPED_KEYS.items():
            if k in config and v not in config:
                config[v] = config[k]

        # coerce value to boolean
        verify = config.get('verify')
        config['verify'] = self.parse_boolean(verify)

        # coerce value to boolean
        retry = config.get('retry')
        config['retry'] = self.parse_boolean(retry)

        max_wait_time = config.get('max_wait_time')
        if max_wait_time is not None:
            config['max_wait_time'] = int(max_wait_time)

        # override Nones with default values if they exist
        for key, val in self.DEFAULTS.items():
            if config.get(key) is None:
                config[key] = val

        # ensure required properties are present
        for key in self.REQUIRED_KEYS:
            if config.get(key) is None:
                raise Exception("Missing config value for %s" % key)

        # check if desired properties are present
        for key in self.DESIRED_KEYS:
            if config.get(key) is None:
                self.logger.warning("Key {} will become mandatory".format(key))

        self.enclave_ids = config.get('enclave_ids')

        if isinstance(self.enclave_ids, str):
            self.enclave_ids = [self.enclave_ids]

        self.token = None



    @staticmethod
    def config_from_file(config_file_path, config_role):
        raise NotImplemented

    def search_indicators(self):
        # TODO add condig
        return SearchIndicator(self)


if __name__ == "main":
    config = {}
    indicators = TruStar(config).search_indicators().set_query_term()\
        .set_start().set_to().query()
    for n in indicators:
        print(n)
