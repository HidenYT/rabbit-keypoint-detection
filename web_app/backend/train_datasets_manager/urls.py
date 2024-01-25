from django.urls import path
from .views import (
    list_train_datasets_view,
    detail_train_dataset_view,
    upload_train_dataset_view,
    edit_train_dataset_view,
    delete_train_dataset_view,
    train_dataset_data_view,
)

app_name = 'train_datasets_manager'

urlpatterns = [
    path('', list_train_datasets_view, name='list_train_datasets'),
    path('upload', upload_train_dataset_view, name='upload_train_dataset'),
    path('edit/<int:id>', edit_train_dataset_view, name='edit_train_dataset'),
    path('delete/<int:id>', delete_train_dataset_view, name='delete_train_dataset'),
    path('<int:id>', detail_train_dataset_view, name='detail_train_dataset'),
    path('<int:id>/download', train_dataset_data_view, name='train_dataset_data'),
]