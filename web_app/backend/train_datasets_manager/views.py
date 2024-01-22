from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def list_train_datasets_view(request):
    return render(request, 'index', {})

@login_required
def detail_train_dataset_view(request, id: int):
    return render(request, 'index', {})

@login_required
def upload_train_dataset_view(request):
    return render(request, 'index', {})

@login_required
def edit_train_dataset_view(request, id: int):
    return render(request, 'index', {})

@login_required
def delete_train_dataset_view(request, id: int):
    return render(request, 'index', {})