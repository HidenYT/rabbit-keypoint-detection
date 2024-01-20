from datetime import datetime
from django.db import models
from train_datasets_manager.models import TrainDataset


class NeuralNetworkType(models.Model):
    name = models.CharField(max_length=100)


class TrainedNeuralNetwork(models.Model):
    name = models.CharField(max_length=200)
    
    file_path = models.CharField(max_length=500)

    started_training_at = models.DateTimeField(default=datetime.now)
    finished_training_at = models.DateTimeField(null=True, blank=True)

    train_dataset = models.ForeignKey(TrainDataset, on_delete=models.DO_NOTHING)

    neural_network_type = models.ForeignKey(NeuralNetworkType, on_delete=models.DO_NOTHING)