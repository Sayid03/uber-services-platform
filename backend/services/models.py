from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    class PricingType(models.TextChoices):
        FIXED = 'fixed', 'Fixed Price'
        HOURLY = 'hourly', 'Hourly Rate'
        NEGOTIABLE = 'negotiable', 'Negotiable'
    
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='services'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='services'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    pricing_type = models.CharField(
        max_length=20,
        choices=PricingType.choices,
        default=PricingType.FIXED
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estimated_duration_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.provider.username}"
