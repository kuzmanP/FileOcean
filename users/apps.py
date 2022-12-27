from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    
    
    #Signals
    def ready(self):
        import users.signals
        
