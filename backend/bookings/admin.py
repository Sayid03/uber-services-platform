from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'service',
        'customer',
        'provider',
        'booking_date',
        'status',
        'estimated_price',
        'created_at',
    )
    list_filter = ('status', 'booking_date', 'created_at')
    search_fields = (
        'service__title',
        'customer__username',
        'provider__username',
        'address',
    )
