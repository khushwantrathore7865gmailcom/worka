from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User_custom(AbstractUser):
    username = models.CharField(max_length=25, unique=True, null=True)
    email = models.EmailField(max_length=30)
    # password = models.CharField(max_length=32,widget=forms.PasswordInput)
    password = models.CharField(max_length=32)
    confirmpass = models.CharField(max_length=32, blank=True)
    is_candidate = models.BooleanField(default=False)
    is_employeer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username