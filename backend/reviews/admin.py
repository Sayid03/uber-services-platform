from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'booking',
        'customer',
        'provider',
        'service',
        'rating',
        'created_at',
    )
    list_filter = ('rating', 'created_at')
    search_fields = (
        'customer__username',
        'provider__username',
        'service__title',
        'comment',
    )
