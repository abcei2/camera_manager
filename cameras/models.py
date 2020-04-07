from django.db import models
from core.model_utils import BaseModel
from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from decimal import Decimal


class Camera(BaseModel):

    FACE_RECOGNTION = 'FR'
    MODEL_DETECTOR = [
        (FACE_RECOGNTION, 'FACE_RECOGNTION'),
    ]
    model_detector = models.CharField(
        max_length=2,
        choices=MODEL_DETECTOR,
        default=FACE_RECOGNTION,
    )

    url = models.URLField()
    # Always use the format 'lon.gitude,lat.itude'
    geopoint = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    web_cam = models.BooleanField(default=False)

    @cached_property
    def coords(self):
        return list(map(lambda x: Decimal(x), self.geopoint.split(',')))

    @cached_property
    def last_frame(self):
        return f"{settings.MEDIA_URL}{self.short_id}.png"

