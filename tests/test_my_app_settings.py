import logging
import os
import unittest
import sys


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(name)s  %(message)s'
)


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'fixtures'))


class ModulesTestCase(unittest.TestCase):

    def setUp(self):
        os.environ.pop('MY_APP_SETTINGS', None)

    def tearDown(self):
        os.environ.pop('MY_APP_SETTINGS', None)
        for module in sys.modules.keys():
            if not module.startswith('my_app'):
                continue
            del sys.modules[module]

    def test_standard(self):

        from my_app import settings

        self.assertTrue(hasattr(settings, 'BASE_DIR'))
        self.assertTrue(hasattr(settings, 'INSTALLED_APPS'))
        self.assertEqual((
            'base',
            'etc',
            'etc.prod1',
            'etc.local',
            'post',
        ), settings.INSTALLED_APPS)

    def test_environ(self):

        os.environ['MY_APP_SETTINGS'] = 'base,post,etc,etc'

        from my_app import settings

        self.assertTrue(hasattr(settings, 'BASE_DIR'))
        self.assertTrue(hasattr(settings, 'INSTALLED_APPS'))
        self.assertEqual((
            'base',
            'post',
            'etc',
            'etc.prod1',
            'etc.local',
        ), settings.INSTALLED_APPS)
