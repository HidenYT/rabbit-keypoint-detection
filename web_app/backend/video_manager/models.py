from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class InferenceVideo(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    file_path = models.CharField(max_length=500)

    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
