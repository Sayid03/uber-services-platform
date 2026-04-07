from django.db import models
from django.contrib.auth.models import AbstractUser

class User (AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'customer', 'Customer'
        PROVIDER = 'provider', 'Provider'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified_provider = models.BooleanField(default=False)

    def __str__(self):
        return self.username
