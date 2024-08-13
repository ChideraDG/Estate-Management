from django.apps import AppConfig


class BuildingOwnersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "building_owners"

    def ready(self):
        import building_owners.signals  
