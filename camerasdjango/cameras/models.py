from django.db import models
from django.conf import settings
from core.model_utils import BaseModel
from django.contrib.auth.models import AbstractUser
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

# from decimal import Decimal

DETECTOR_TYPES = (
    ('face_recogntion', _('Face recognition')),
)


class User(AbstractUser, BaseModel):
    # id = models.UUIDField
    # username
    # password
    # first_name
    # last_name
    # is_active
    # is_staff
    # is_superuser
    # last_login
    # date_joined
    email = models.EmailField('email address', unique=True)
    debug_toolbar = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __json__(self, *attrs):
        return {
            **self.attrs(
                'id',
                'email',
                'username',
                'first_name',
                'last_name',
                'date_joined',
                'is_active',
                'is_staff',
                'is_superuser',
                'is_authenticated',
            ),
            'str': str(self),
            **(self.attrs(*attrs) if attrs else {}),
        }


class Camera(BaseModel):

    #RELATION OF CAMERA TO USER
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    detector_type = models.CharField(
        max_length=32,
        choices=DETECTOR_TYPES,
        default='face_recognition',
    )

    url = models.URLField()
    # Always use the format 'lon.gitude,lat.itude'
    geopoint = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    web_cam = models.BooleanField(default=False)

    # @cached_property
    # def coords(self):
    #     return list(map(lambda x: Decimal(x), self.geopoint.split(',')))

    # @cached_property
    # def latlon_geopoint(self):
    #     gpoint = self.coords
    #     gpoint.reverse()
    #     return ','.join([str(gp) for gp in gpoint])

    @cached_property
    def last_frame(self):
        return f"{settings.MEDIA_URL}{self.short_id}.png"

    @cached_property
    def title(self):
        return f'{_("Web cam")} {self.url}' if self.web_cam else self.url
