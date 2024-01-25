from django.dispatch import receiver
from django.db import models
from .models import InferenceVideo
import os


@receiver(models.signals.post_delete, sender=InferenceVideo)
def auto_delete_file_on_delete(sender, instance: InferenceVideo, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

@receiver(models.signals.pre_save, sender=InferenceVideo)
def auto_delete_file_on_change(sender, instance: InferenceVideo, **kwargs):
    if instance.pk is None:
        return False
    try:
        old_file = InferenceVideo.objects.get(pk=instance.pk).file
    except InferenceVideo.DoesNotExist:
        return False
    new_file = instance.file
    if old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)