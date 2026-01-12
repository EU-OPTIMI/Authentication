from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
import uuid

class User(AbstractUser):
    """
    Custom user model.
    Extends Django's AbstractUser with provider and consumer flags.
    """
    is_provider = models.BooleanField(default=False)
    is_consumer = models.BooleanField(default=False)

    def __str__(self):
        return self.username or self.email or str(self.id)


class ProvidedOffer(models.Model):
    """
    Stores each offer provided by a user as a separate row.
    This avoids overwriting previous offers when adding new ones.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="provided_offers"
    )
    offer_id = models.UUIDField()  # Or models.CharField if your offer IDs are strings
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "offer_id")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.offer_id} by {self.user}"
