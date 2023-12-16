from django.apps import AppConfig


class UnreturnedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'unreturned'
