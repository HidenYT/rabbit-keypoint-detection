# Generated by Django 5.0.1 on 2024-01-20 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video_manager', '0002_alter_inferencevideo_file_path'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inferencevideo',
            old_name='file_path',
            new_name='file',
        ),
    ]