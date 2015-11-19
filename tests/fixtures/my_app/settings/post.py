import __settings__

from __settings__ import INSTALLED_APPS


assert hasattr(__settings__, 'BASE_DIR'), 'BASE_DIR required'


INSTALLED_APPS += (
    'post',
)
