#!/usr/bin/env python
import os
import codecs

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))


setup(
    name='django-compose-settings',
    version=codecs.open(os.path.join(here, 'VERSION'), encoding='utf-8').read().strip(),
    description='Django composable settings loader.',
    long_description=codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    keywords=[
        'django',
        'settings',
    ],
    author='PeopleDoc',
    author_email='rd@novapost.fr',
    url='https://github.com/novafloss/django-compose-settings',
    license='MIT',
    extras_require={
        'release': [
            'wheel',
            'zest.releaser'
        ],
        'tests': [
            'flake8'
        ]
    },
    packages=[
        'django_compose_settings'
    ],
)
