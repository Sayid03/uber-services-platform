from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework.exceptions import PermissionDenied

from .models import Booking
from .serializers import BookingSerializer, BookingStatusUpdateSerializer

class BookingListCreateAPIView(generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'service', 'provider']
    ordering_fields = ['booking_date', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        return BookingSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'provider':
            return Booking.objects.select_related(
                'customer', 'provider', 'service'
            ).filter(provider=user)

        return Booking.objects.select_related(
            'customer', 'provider', 'service'
        ).filter(customer=user)

    def perform_create(self, serializer):
        user = self.request.user
        service = serializer.validated_data['service']

        if user.role != 'customer':
            raise PermissionDenied('Only customers can create bookings.')

        serializer.save(
            customer=user,
            provider=service.provider,
            estimated_price=service.price
        )

class BookingDetailAPIView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Booking.objects.select_related(
            'customer', 'provider', 'service'
        ).filter(
            models.Q(customer=user) | models.Q(provider=user)
        )
    
class BookingStatusUpdateAPIView(generics.UpdateAPIView):
    serializer_class = BookingStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Booking.objects.select_related(
            'customer', 'provider', 'service'
        ).filter(provider=user)

    def perform_update(self, serializer):
        booking = self.get_object()
        user = self.request.user

        if booking.provider != user:
            raise PermissionDenied('Only the provider can update booking status.')

        serializer.save()
