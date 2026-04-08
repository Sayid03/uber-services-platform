from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters

from .models import Review
from .serializers import ReviewSerializer

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['provider', 'service', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Review.objects.select_related(
            'booking', 'customer', 'provider', 'service'
        ).all()

        provider_id = self.request.query_params.get('provider')
        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)

        service_id = self.request.query_params.get('service')
        if service_id:
            queryset = queryset.filter(service_id=service_id)

        return queryset
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        booking = serializer.validated_data['booking']

        serializer.save(
            customer=self.request.user,
            provider=booking.provider,
            service=booking.service,
        )

class ReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = Review.objects.select_related(
        'booking', 'customer', 'provider', 'service'
    ).all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
