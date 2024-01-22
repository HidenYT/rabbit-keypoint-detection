from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from utils.file_uploads import default_upload_path
from django.conf import settings

def train_dataset_upload_path(instance: "TrainDataset", filename: str) -> str:
    return default_upload_path(settings.TRAIN_DATASET_UPLOAD_DIR, instance.user, filename)

class TrainDataset(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    file = models.FileField(upload_to=train_dataset_upload_path)

    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Skeleon(models.Model):
    kp_relations = models.JSONField()

    train_dataset = models.OneToOneField(TrainDataset, on_delete=models.CASCADE)
    

class SkeletonKeypoint(models.Model):
    name = models.CharField(max_length=100)
    skeleton = models.ForeignKey(Skeleon, on_delete=models.CASCADE)