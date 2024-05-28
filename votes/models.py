from django.db import models
from django.conf import settings

from onions.models import Onion


# Create your models here.
class Vote(models.Model):
    onion = models.ForeignKey(Onion, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(
        choices=(('Up', 'Up'), ('Down', 'Down')),
        max_length=4,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
