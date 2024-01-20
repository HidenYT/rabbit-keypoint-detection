from datetime import datetime
from django.db import models
from model_training.models import TrainedNeuralNetwork
from video_manager.models import InferenceVideo


class InferredKeypoints(models.Model):
    keypoints = models.JSONField()

    started_inference_at = models.DateTimeField(default=datetime.now)
    finished_inference_at = models.DateTimeField(null=True, blank=True)

    trained_neural_network = models.ForeignKey(TrainedNeuralNetwork, on_delete=models.DO_NOTHING)

    inference_video = models.ForeignKey(InferenceVideo, on_delete=models.DO_NOTHING)