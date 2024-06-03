from django.db import models
from django.conf import settings
from pgvector.django import VectorField
from django.contrib.postgres.fields import ArrayField, JSONField

class Onion(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    color = models.CharField(choices=(('Orange','Orange'), ('Purple','Purple')), max_length=10)
    parent_onion = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='child_onions')
    num_of_views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OnionVersus(models.Model):
    ov_title = models.CharField(max_length=30, default="No title")
    orange_onion = models.ForeignKey(Onion, on_delete=models.CASCADE, related_name='orange_onion')
    purple_onion = models.ForeignKey(Onion, on_delete=models.CASCADE, related_name='purple_onion')
    title_embedding = VectorField(dimensions=768)
    orange_embedding = VectorField(dimensions=768)
    purple_embedding = VectorField(dimensions=768)
    created_at = models.DateTimeField(auto_now_add=True)

class OnionViews(models.Model):
    onion = models.ForeignKey(Onion, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
