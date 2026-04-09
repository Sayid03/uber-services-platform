from django.utils import timezone
from celery import shared_task
from .models import Booking

@shared_task
def cancel_expired_pending_bookings():
    expired_bookings = Booking.objects.filter(
        status='pending',
        booking_date__lt=timezone.now()
    )

    updated_count = expired_bookings.update(status='cancelled')
    return f"{updated_count} expired pending bookings cancelled."