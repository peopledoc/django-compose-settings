import logging
import os

from .modules import update_settings  # noqa


logger = logging.getLogger('django_compose_settings')


def etc_loader(prefix, root='/etc'):

    import __settings__

    # List settings files from /etc/{prefix}
    etcdir = os.path.join(root, prefix)
    mainfile = os.path.join(etcdir, 'settings.py')
    dotd = os.path.join(etcdir, 'settings.d')

    logger.debug('etcdir: %s', etcdir)

    etcfiles = []

    if os.path.exists(mainfile):
        etcfiles.append(mainfile)

    if os.path.isdir(dotd):
        etcfiles += sorted([
            os.path.join(dotd, f) for f in os.listdir(dotd)
        ])

    logger.debug('etcfiles: %s', etcfiles)

    # Now execfile each to fetch settings.
    for file_ in etcfiles:

        if '/README' in file_:
            continue

        if not file_.endswith('.py'):
            logger.warning("Loads only *.py files. Ignoring %s.", file_)
            continue

        globals_ = dict(globals(), **{
            '__name__': '__settings__',
            '__file__': file_,
        })

        try:
            # Collect variables in globals_ dictionnary
            with open(file_) as f:
                exec(f.read(), globals_)
        except IOError as e:
            # ImportError are handled by django.
            raise ImportError(e.message)

        update_settings(__settings__, globals_)
        logger.info("Loaded %s", file_)

    # Fetch only settings from current modules.
    return {k: v for k, v in vars(__settings__).items() if k.isupper()}
