from django.apps import AppConfig
from batch.Main import Main


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        Main()


