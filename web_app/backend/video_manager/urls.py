from django.urls import path
from .views import (
    list_inference_videos_view,
    detail_inference_video_view,
    upload_inference_video_view,
    edit_inference_video_view,
    delete_inference_video_view,
    inference_video_data_view,
)


app_name = "video_manager"

urlpatterns = [
    path("", list_inference_videos_view, name="list_inference_videos"),
    path("<int:id>", detail_inference_video_view, name="detail_inference_video"),
    path("upload", upload_inference_video_view, name="upload_inference_video"),
    path("edit/<int:id>", edit_inference_video_view, name="edit_inference_video"),
    path("delete/<int:id>", delete_inference_video_view, name="delete_inference_video"),
    path("<int:id>/download", inference_video_data_view, name="inference_video_data")

]