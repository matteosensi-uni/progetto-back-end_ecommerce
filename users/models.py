from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    address = models.CharField(max_length=255, blank=True)    
    phone = models.CharField(max_length=20, blank=True)

    
    def is_manager(self):
            return self.groups.filter(name="Manager").exists()
