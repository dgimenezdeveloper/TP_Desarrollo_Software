from django.apps import AppConfig


class AppLuminovaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App_Luminova'
    
    def ready(self):
        print("AppLuminovaConfig.ready() ejecutado. Importando señales...") # DEBUG
        import App_Luminova.signals
        print("Señales importadas.") # DEBUG