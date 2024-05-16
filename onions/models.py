from django.db import models
from django.conf import settings
# Create your models here.
class Onion(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    num_of_views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OnionVersus(models.Model):
    orange_onion = models.ForeignKey(Onion, on_delete=models.CASCADE, related_name='orange_onion')
    purple_onion = models.ForeignKey(Onion, on_delete=models.CASCADE, related_name='purple_onion')
    created_at = models.DateTimeField(auto_now_add=True)
