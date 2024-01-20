from datetime import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from utils.file_uploads import default_upload_path

def inference_video_upload_path(instance: "InferenceVideo", filename: str) -> str:
    return default_upload_path(settings.INFERENCE_VIDEO_UPLOAD_DIR, instance.user, filename)

class InferenceVideo(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    file = models.FileField(upload_to=inference_video_upload_path)

    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
