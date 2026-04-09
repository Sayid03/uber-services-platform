from django.urls import path
from .views import (
    BookingListCreateAPIView,
    BookingDetailAPIView,
    BookingStatusUpdateAPIView,
)

urlpatterns = [
    path('', BookingListCreateAPIView.as_view(), name='booking-list-create'),
    path('<int:id>/', BookingDetailAPIView.as_view(), name='booking-detail'),
    path('<int:id>/status/', BookingStatusUpdateAPIView.as_view(), name='booking-status-update'),
]