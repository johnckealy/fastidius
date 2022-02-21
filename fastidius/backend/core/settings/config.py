import os
import sys
from functools import lru_cache
from typing import Union

from .dev import SettingsDev
from .prod import SettingsProd


environments: dict = {
    'dev': SettingsDev,
    'prod': SettingsProd,
}


@lru_cache
def get_app_settings() -> Union[SettingsDev, SettingsProd]:
    """All settings are routed through here on startup of the app or the test suite."""
    environment = os.environ.get('BASE_ENVIRONMENT')

    # If pytest was invoked, then use the test suite settings
    if environment != 'ci' and 'pytest' in sys.argv[0]:
        environment = 'test'

    if environment is None:
        raise ValueError("The BASE_ENVIRONMENT variable has not been set")

    config = environments[environment]
    return config()


settings = get_app_settings()
