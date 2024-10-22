from django.apps import AppConfig


class MaintenancesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenances"
    
    def ready(self):
        import maintenances.signals