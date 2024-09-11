from django.apps import AppConfig


########################################################################################
# Configuración de la aplicación 'accounts'.
class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myApp'
