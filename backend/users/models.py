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
    
class ProviderProfile(models. Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='provider_profile'
    )
    bio = models.TextField(blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    region = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Provider Profile - {self.user.username}"