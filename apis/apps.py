from django.apps import AppConfig


class ApisConfig(AppConfig):
    name = 'apis'
   #Signals
    def ready(self):
        import apis.signals