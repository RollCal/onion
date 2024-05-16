from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(unique=True, max_length=10)
    gender = models.CharField(
        choices=(('M', '남성'), ('F', '여성')),
        max_length=1,
    )
    birth = models.DateField(null=True, blank=True)
    karma = models.IntegerField(default=0)