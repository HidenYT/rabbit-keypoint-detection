from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class TrainDataset(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    file_path = models.CharField(max_length=500)

    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Skeleon(models.Model):
    kp_relations = models.JSONField()

    train_dataset = models.OneToOneField(TrainDataset, on_delete=models.CASCADE)
    

class SkeletonKeypoint(models.Model):
    name = models.CharField(max_length=100)
    skeleton = models.ForeignKey(Skeleon, on_delete=models.CASCADE)