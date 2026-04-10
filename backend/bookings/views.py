from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters

from .models import Booking
from .serializers import BookingSerializer, BookingStatusUpdateSerializer
from .permissions import IsCustomer, IsBookingParticipant, IsBookingProvider

class BookingListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List bookings for the authenticated user.
    Customers see their bookings; providers see bookings for their services.
    POST: Create a new booking as a customer.
    """
    queryset = Booking.objects.none()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'service', 'provider']
    ordering_fields = ['booking_date', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        return BookingSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsCustomer()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()

        user = self.request.user

        if not user.is_authenticated:
            return Booking.objects.none()

        if user.role == 'provider':
            return Booking.objects.select_related(
                'customer', 'provider', 'service'
            ).filter(provider=user)

        return Booking.objects.select_related(
            'customer', 'provider', 'service'
        ).filter(customer=user)

    def perform_create(self, serializer):
        service = serializer.validated_data['service']
        serializer.save(
            customer=self.request.user,
            provider=service.provider,
            estimated_price=service.price
        )

class BookingDetailAPIView(generics.RetrieveAPIView):
    """
    GET: Retrieve a booking only if the authenticated user is the customer or provider involved.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsBookingParticipant]
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.select_related(
            'customer', 'provider', 'service'
        ).filter(
            models.Q(customer=user) | models.Q(provider=user)
        )
    
class BookingStatusUpdateAPIView(generics.UpdateAPIView):
    """
    PATCH: Update booking status as the provider assigned to that booking.
    """
    serializer_class = BookingStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsBookingProvider]
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return Booking.objects.select_related(
            'customer', 'provider', 'service'
        )
