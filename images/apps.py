from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'
    def ready(self):
        from . import signals
