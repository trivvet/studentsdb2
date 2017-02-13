from django.db import models
from django.contrib.auth.models import User

class StProfile(models.Model):

    user_profile = models.OneToOneField(User)
    
    mobile_phone = models.CharField(
        verbose_name="Mobile Phone",
        max_length=12,
        blank=True)
