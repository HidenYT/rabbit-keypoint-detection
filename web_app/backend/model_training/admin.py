from django.contrib import admin
from .models import NeuralNetworkType, TrainedNeuralNetwork


admin.site.register(NeuralNetworkType)
admin.site.register(TrainedNeuralNetwork)