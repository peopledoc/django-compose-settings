import os.path

from django_compose_settings import etc_loader


ETC_DIR = os.path.realpath(os.path.join(
    os.path.abspath(__file__),
    '..',
    '..',
    '..',
    'etc',
))


locals().update(etc_loader(prefix='my_app', root=ETC_DIR))
