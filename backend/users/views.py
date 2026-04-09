from django.db.models import Avg, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema

from .models import User
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ProviderProfileSerializer,
    ProviderListSerializer,
)
from .filters import ProviderFilter

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema(responses=UserSerializer)
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class ProviderProfileUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProviderProfileSerializer

    def get_object(self):
        user = self.request.user
        if user.role != 'provider':
            raise PermissionDenied('Only providers can access this profile.')
        return user.provider_profile

class ProviderListAPIView(generics.ListAPIView):
    """
    GET: List providers with profile info, rating, and filtering options.
    """
    serializer_class = ProviderListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProviderFilter
    search_fields = ['username', 'first_name', 'last_name', 'provider_profile__region', 'provider_profile__district']
    ordering_fields = ['average_rating', 'reviews_count', 'services_count', 'username']
    ordering = ['-average_rating', '-reviews_count']

    def get_queryset(self):
        return User.objects.filter(role='provider').select_related('provider_profile').annotate(
            average_rating=Avg('received_reviews__rating'),
            reviews_count=Count('received_reviews', distinct=True),
            services_count=Count('services', distinct=True),
        )