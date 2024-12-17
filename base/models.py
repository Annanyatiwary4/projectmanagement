from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_candidate = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email

from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)  # Example additional field
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Example additional field
    token = models.CharField(max_length=32, blank=True, null=True)  

    def __str__(self):
        return f'{self.user.username} Profile'
