from django import forms
from .models import TrainDataset

class DatasetUploadForm(forms.ModelForm):
    class Meta:
        model = TrainDataset
        exclude = ['created_at', 'updated_at', 'user']

class DatasetEditForm(forms.ModelForm):
    class Meta:
        model = TrainDataset
        exclude = ['created_at', 'updated_at', 'user', 'file']
    file = forms.FileField(required=False)
    
class DatasetDeleteForm(forms.Form):
    pass