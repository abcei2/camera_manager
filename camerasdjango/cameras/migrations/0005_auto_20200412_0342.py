# Generated by Django 3.0.5 on 2020-04-12 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cameras', '0004_auto_20200406_2139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camera',
            name='model_detector',
        ),
        migrations.AddField(
            model_name='camera',
            name='detector_type',
            field=models.CharField(choices=[('face_recogntion', 'Face recognition')], default='face_recognition', max_length=32),
        ),
    ]