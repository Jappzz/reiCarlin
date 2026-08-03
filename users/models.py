from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    #modelo que o usuario deve terA
    email = models.EmailField(unique=True, max_length=255)
    is_employee = models.BooleanField(default=False)



