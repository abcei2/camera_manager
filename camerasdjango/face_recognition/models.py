from django.db import models

from core.model_utils import BaseModel
from cameras.models import Camera


class Face(BaseModel):
    name = models.CharField(max_length=64, unique=True)


class FaceRecognitionReport(BaseModel):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    face = models.ForeignKey(Face, on_delete=models.CASCADE)
