from django.db import models
from django.contrib.auth.models import AbstractUser 

class CustomUser(AbstractUser):
	cargo =models.CharField(max_length=50)
	edad = models.PositiveIntegerField(null=True, blank=True)

	
