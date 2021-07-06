import importlib
import inspect
import logging
import os
import sys
import traceback
import types


logger = logging.getLogger('django_compose_settings')


def update_settings(current, new_settings):
    # Note that we do not clear settings. We use same behaviour as .d
    # directory: modules are loaded in order, settings are merged.
    vars(current).update(
        {k: v for k, v in new_settings.items() if k.isupper()}
    )


def modules_loader(prefix, default=''):

    envvar = '{}_SETTINGS'.format(prefix.upper())
    logger.debug('envvar: %s', os.environ.get(envvar))

    modules = os.environ.get(envvar, default).split(',')
    if not modules:
        logger.warning('No settings to load!')
        sys.exit(1)

    # uniqify, preserving order.. From
    # http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order  # noqa
    seen = set()
    modules = [x for x in modules if not (x in seen or seen.add(x))]

    logger.debug('modules: %s', modules)

    # Virtual module containing current settings, while loading multiple
    # settings files. By importing __settings__ in any settings file, you can
    # update a settings before it is available in django.conf.settings, without
    # knowing the inclusion order of settings.
    current_name = '__settings__'

    if current_name in sys.modules:
        logger.critical("Settings inception!")
        frame = inspect.currentframe()
        logger.error(
            "Traceback:\n" +
            ''.join(traceback.format_stack(frame))
        )
        logger.error("%r", sys.modules.keys())
        sys.exit(1)

    current = types.ModuleType(current_name)
    sys.modules[current_name] = current

    # Marshall loading settings from python modules
    for name in modules:

        fullname = '{0}.settings.{1}'.format(prefix, name.strip())
        try:
            module = importlib.import_module(fullname)
        except Exception:
            logger.exception("Failed to load setting module '%s'", fullname)
            sys.exit(1)

        update_settings(current, vars(module))
        logger.info("Loaded %s", fullname)

        del sys.modules[fullname]

    # Fetch only settings from current modules.
    settings = {k: v for k, v in vars(current).items() if k.isupper()}

    # Drop __settings__, code must now use regular django.conf.settings module.
    del sys.modules[current_name]

    return settings
