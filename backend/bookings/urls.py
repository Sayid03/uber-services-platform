from django.urls import path
from .views import (
    BookingListCreateAPIView,
    BookingDetailAPIView,
    BookingStatusUpdateAPIView,
)

urlpatterns = [
    path('', BookingListCreateAPIView.as_view(), name='booking-list-create'),
    path('<int:pk>/', BookingDetailAPIView.as_view(), name='booking-detail'),
    path('<int:pk>/status/', BookingStatusUpdateAPIView.as_view(), name='booking-status-update'),
]