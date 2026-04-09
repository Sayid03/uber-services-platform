from django.utils import timezone
from celery import shared_task
from django.db.utils import OperationalError, ProgrammingError
from .models import Booking

@shared_task
def cancel_expired_pending_bookings():
    try:
        expired_bookings = Booking.objects.filter(
            status='pending',
            booking_date__lt=timezone.now()
        )
        updated_count = expired_bookings.update(status='cancelled')
        return f"{updated_count} expired pending bookings cancelled."
    except (OperationalError, ProgrammingError) as e:
        return f"Task skipped because database is not ready: {str(e)}"