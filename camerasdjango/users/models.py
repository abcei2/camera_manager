from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.contrib.sessions.models import Session

class CustomUser(AbstractUser):
	cargo =models.CharField(max_length=50)
	edad = models.PositiveIntegerField(null=True, blank=True)




# class UserSession(models.Model):
#     user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#     session = models.ForeignKey(Session,on_delete=models.CASCADE)    

	
