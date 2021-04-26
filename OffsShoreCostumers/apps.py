from django.apps import AppConfig


class OffsshorecostumersConfig(AppConfig):
    name = 'OffsShoreCostumers'

    def ready(self):
        import OffsShoreCostumers.signals