from django.contrib import admin
from train_datasets_manager.forms import DatasetUploadForm
from .models import TrainDataset, Skeleon, SkeletonKeypoint


admin.site.register(TrainDataset)
admin.site.register(Skeleon)
admin.site.register(SkeletonKeypoint)