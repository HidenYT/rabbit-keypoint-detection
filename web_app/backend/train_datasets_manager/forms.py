from django import forms
from .models import TrainDataset

class DatasetUploadForm(forms.ModelForm):
    class Meta:
        model = TrainDataset
        exclude = ['created_at', 'updated_at', 'user']
    
