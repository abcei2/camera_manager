from django.db import models
from cameras.models import Camera
from django.contrib.postgres.fields import ArrayField


class FaceRecognitionCamera(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)

class FaceRecognitionCamera_reports(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    face_detected=models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    



