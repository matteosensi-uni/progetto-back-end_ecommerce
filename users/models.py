from django.db import models
from django.contrib.auth.models import AbstractUser

#modello per gli utenti
class CustomUser(AbstractUser):
    
    email = models.EmailField(blank=False, null=False) #ridefinisco il campo email di abstractuser per renderlo obbligatorio
    address = models.CharField(max_length=255, blank=True)    
    phone = models.CharField(max_length=20, blank=True)

    def is_manager(self):
            return self.groups.filter(name="Manager").exists()
