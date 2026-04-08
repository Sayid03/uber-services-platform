from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters

from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsCustomer

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List reviews with optional filtering by provider, service, and rating.
    POST: Create a review as a customer for a completed booking.
    """
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['provider', 'service', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_queryset(self):
        return Review.objects.select_related(
            'booking', 'customer', 'provider', 'service'
        ).all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsCustomer()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        booking = serializer.validated_data['booking']
        serializer.save(
            customer=self.request.user,
            provider=booking.provider,
            service=booking.service,
        )

class ReviewDetailAPIView(generics.RetrieveAPIView):
    """
    GET: Retrieve a single review.
    """
    queryset = Review.objects.select_related(
        'booking', 'customer', 'provider', 'service'
    )
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
