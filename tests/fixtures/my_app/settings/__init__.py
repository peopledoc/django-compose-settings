from django_compose_settings import modules_loader

locals().update(modules_loader(prefix='my_app', default='base,etc,post'))
