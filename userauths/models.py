from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=200, unique=False, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def str(self) -> str:
        return self.username