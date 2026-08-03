from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    #modelo que o usuario deve ter
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=128)
    is_employee = models.BooleanField(default=False)



