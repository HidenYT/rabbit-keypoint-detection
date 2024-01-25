from django import forms
from .models import InferenceVideo


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = InferenceVideo
        exclude = ["created_at", "updated_at", "user"]

class VideoEditForm(forms.ModelForm):
    class Meta:
        model = InferenceVideo
        exclude = ["created_at", "updated_at", "user", "file"]
    file = forms.FileField(required=False)