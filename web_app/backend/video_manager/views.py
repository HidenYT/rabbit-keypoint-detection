from datetime import datetime
import os
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django_sendfile import sendfile
from django.urls import reverse

from .forms import VideoEditForm, VideoUploadForm
from .models import InferenceVideo


def get_video(request: HttpRequest, id: int):
    return get_object_or_404(InferenceVideo, pk=id, user=request.user)

@login_required
def list_inference_videos_view(request: HttpRequest):
    videos = InferenceVideo.objects.filter(user=request.user)
    ctx = {
        "videos": videos,
    }
    return render(request, "video_manager/list.html", ctx)

@login_required
def detail_inference_video_view(request: HttpRequest, id: int):
    video = get_video(request, id)
    return render(request, 'video_manager/detail.html', {"video": video})

@login_required
def upload_inference_video_view(request: HttpRequest):
    form = VideoUploadForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            video = InferenceVideo()
            video.name = form.cleaned_data['name']
            video.description = form.cleaned_data['description']
            video.user = request.user
            video.file = request.FILES['file']
            video.save()
            return redirect(reverse('video_manager:detail_inference_video', kwargs={"id":video.pk}))
    return render(request, 'video_manager/upload.html', {"form": form})

@login_required
def edit_inference_video_view(request: HttpRequest, id: int):
    video = get_video(request, id)
    form = VideoEditForm(request.POST or None, request.FILES or None, instance=video)
    if request.method == "POST":
        if form.is_valid():
            video.name = form.cleaned_data['name']
            video.description = form.cleaned_data['description']
            if request.FILES:
                video.file = request.FILES['file']
            video.updated_at = datetime.now()
            video.save()
    return render(request, 'video_manager/edit.html', {"form": form, "video": video})

@login_required
def delete_inference_video_view(request: HttpRequest, id: int):
    video = get_video(request, id)
    if request.method == "POST":
        video.delete()
        return redirect(reverse("video_manager:list_inference_videos"))
    return render(request, "video_manager/delete.html", {"video": video})

@login_required
def inference_video_data_view(request: HttpRequest, id: int):
    video = get_video(request, id)
    _, ext = os.path.splitext(video.file.path)
    return sendfile(request, 
                    video.file.path, 
                    attachment=True, 
                    attachment_filename=f'Inference video {video.name}{ext}',
                    )