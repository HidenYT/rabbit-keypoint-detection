from django.apps import AppConfig


class ModelInferenceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'model_inference'
