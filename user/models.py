from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class MyUser(AbstractUser):
    age = models.IntegerField()
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=True)
    REQUIRED_FIELDS = ["age", "can_be_contacted", "can_data_be_shared"]
