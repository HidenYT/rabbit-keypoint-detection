# Generated by Django 5.0.1 on 2024-01-20 12:31

import train_datasets_manager.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('train_datasets_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traindataset',
            name='file_path',
            field=models.FileField(upload_to=train_datasets_manager.models.train_dataset_upload_path),
        ),
    ]