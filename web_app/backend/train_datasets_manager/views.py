from datetime import datetime
import os
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django_sendfile import sendfile
from django.urls import reverse
from functools import wraps

from train_datasets_manager.forms import DatasetDeleteForm, DatasetEditForm, DatasetUploadForm
from .models import TrainDataset

def get_dataset(request, id: int) -> TrainDataset:
    return get_object_or_404(TrainDataset, pk=id, user=request.user)

@login_required
def list_train_datasets_view(request):
    datasets = TrainDataset.objects.filter(user_id=request.user.id)
    ctx = {
        "datasets": datasets,
    }
    return render(request, 'train_datasets_manager/list.html', ctx)

@login_required
def detail_train_dataset_view(request, id: int):
    dataset = get_dataset(request, id)
    return render(request, 'train_datasets_manager/detail.html', {"dataset": dataset})

@login_required
def upload_train_dataset_view(request):
    form = DatasetUploadForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            dataset = TrainDataset()
            dataset.name = form.cleaned_data['name']
            dataset.description = form.cleaned_data['description']
            dataset.user = request.user
            dataset.save()
            return redirect(reverse('train_datasets:view_train_dataset', kwargs={"id":dataset.pk}))
    return render(request, 'train_datasets_manager/upload.html', {"form": form})

@login_required
def edit_train_dataset_view(request, id: int):
    dataset = get_dataset(request, id)
    form = DatasetEditForm(request.POST or None, request.FILES or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            dataset.name = form.cleaned_data['name']
            dataset.description = form.cleaned_data['description']
            if request.FILES:
                dataset.file = request.FILES['file']
            dataset.updated_at = datetime.now()
            dataset.save()
    return render(request, 'train_datasets_manager/edit.html', {"form": form, "dataset": dataset})

@login_required
def delete_train_dataset_view(request, id: int):
    dataset = get_dataset(request, id)
    form = DatasetDeleteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        dataset.delete()
        return redirect(reverse("train_datasets:train_datasets_list"))
    return render(request, "train_datasets_manager/delete.html", {"dataset": dataset})

@login_required
def train_dataset_data_view(request, id: int):
    dataset = get_dataset(request, id)
    _, ext = os.path.splitext(dataset.file.path)
    return sendfile(request, 
                    dataset.file.path, 
                    attachment=True, 
                    attachment_filename=f'Train dataset {dataset.name}{ext}',
                    )