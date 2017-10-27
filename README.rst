=================================
Django composable settings loader
=================================


.. image:: https://circleci.com/gh/novafloss/django-compose-settings.svg?style=shield
   :target: https://circleci.com/gh/novafloss/django-compose-settings
   :alt: We are under CI!!

Aims to compose your settings from python modules and python scripts in /etc.

In your ``my_app/settings/__init__.py`` call the loader::

    from django_compose_settings import modules_loader

    locals().update(modules_loader(prefix='my_app', default='base,etc,post'))


In ``my_app/settings/base.py`` define default values as usual, ex::

    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # ...


In ``my_app/settings/etc.py`` call the etc loader::

    from django_compose_settings import etc_loader

    locals().update(etc_loader(prefix='my_app'))


You can validate settings in ``my_app/settings/post.py`` as follow::

    import __settings__

    assert hasattr(__settings__, 'BASE_DIR'), 'BASE_DIR required'


Etc settings
============

Here is a sample tree of your ``/etc/my_app``::

    /etc/my_app/
    ├── settings.d
    │   ├── 00_prod1.py
    │   └── 99_local.py
    └── settings.py

Each ``.py`` file is a regular *composable* settings file as ``post.py`` above.


MY_APP_SETTINGS
===============

You can override your settings with a specific SETTINGS environment variable
for your app as follow::

    $ MY_APP_SETTINGS=base,post python

    >>> import logging
    >>> logging.basicConfig(
    ...     level=logging.INFO,
    ...     format='%(asctime)s %(levelname)-8s %(name)s  %(message)s'
    ... )

    >>> import os
    >>> import sys
    >>> sys.path.append(os.path.join(os.path.abspath('tests'), 'fixtures'))

    >>> from my_app import settings

    2015-11-23 10:59:09,964 INFO     django_compose_settings  Loaded my_app.settings.base
    2015-11-23 10:59:09,964 INFO     django_compose_settings  Loaded my_app.settings.post

