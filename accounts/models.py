from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_provider = models.BooleanField(default=False)
    is_consumer = models.BooleanField(default=False)
    provider_id = models.CharField(max_length=100, blank=True, null=True)
    consumer_id = models.CharField(max_length=100, blank=True, null=True)

    # Store offer IDs as a list in JSONField
    provided_offer_ids = models.JSONField(default=list, blank=True)
    consumed_offer_ids = models.JSONField(default=list, blank=True)
