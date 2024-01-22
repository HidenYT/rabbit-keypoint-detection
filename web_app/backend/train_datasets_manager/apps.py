from django.apps import AppConfig


class TrainDatasetsManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'train_datasets_manager'

    def ready(self) -> None:

        from . import signals
        
        return super().ready()
