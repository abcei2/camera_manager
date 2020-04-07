# Generated by Django 2.2.6 on 2020-04-05 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cameras', '0001_initial'),
        ('face_recognition', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaceRecognitionCamera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cameras.Camera')),
            ],
        ),
        migrations.CreateModel(
            name='FaceRecognitionCamera_reports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('face_detected', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cameras.Camera')),
            ],
        ),
        migrations.RemoveField(
            model_name='pedestriancamera_reports',
            name='camera',
        ),
        migrations.DeleteModel(
            name='PedestrianCamera',
        ),
        migrations.DeleteModel(
            name='PedestrianCamera_reports',
        ),
    ]
