from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from train_datasets_manager.forms import DatasetUploadForm
from .models import TrainDataset

@login_required
def list_train_datasets_view(request):
    datasets = TrainDataset.objects.filter(user_id=request.user.id)
    ctx = {
        "datasets": datasets,
    }
    return render(request, 'train_datasets_manager/list.html', ctx)

@login_required
def detail_train_dataset_view(request, id: int):
    model = TrainDataset.objects.get(pk=id)
    return render(request, 'train_datasets_manager/detail.html', {"dataset": model})

@login_required
def upload_train_dataset_view(request):
    form = DatasetUploadForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            dataset = TrainDataset()
            dataset.name = form.cleaned_data['name']
            dataset.description = form.cleaned_data['description']
            dataset.file = request.FILES['file']
            dataset.user = request.user
            dataset.save()
    return render(request, 'train_datasets_manager/upload.html', {"form": form})

@login_required
def edit_train_dataset_view(request, id: int):
    return render(request, 'index', {})

@login_required
def delete_train_dataset_view(request, id: int):
    return render(request, 'index', {})