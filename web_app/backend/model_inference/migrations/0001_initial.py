# Generated by Django 5.0.1 on 2024-01-20 11:20

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('model_training', '0001_initial'),
        ('video_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InferredKeypoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keypoints', models.JSONField()),
                ('started_inference_at', models.DateTimeField(default=datetime.datetime.now)),
                ('finished_inference_at', models.DateTimeField(blank=True, null=True)),
                ('inference_video', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='video_manager.inferencevideo')),
                ('trained_neural_network', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='model_training.trainedneuralnetwork')),
            ],
        ),
    ]