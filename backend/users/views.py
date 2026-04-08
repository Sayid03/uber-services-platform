from django.db.models import Avg, Count
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from .models import User
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ProviderProfileSerializer,
    ProviderListSerializer,
)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class ProviderProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProviderProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user

        if user.role != 'provider':
            raise PermissionDenied('Only providers can access this profile.')

        return user.provider_profile

class ProviderListAPIView(generics.ListAPIView):
    serializer_class = ProviderListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = User.objects.filter(role='provider').select_related('provider_profile').annotate(
            average_rating=Avg('received_reviews__rating'),
            reviews_count=Count('received_reviews', distinct=True),
            services_count=Count('services', distinct=True),
        )

        verified = self.request.query_params.get('verified')
        if verified is not None:
            if verified.lower() == 'true':
                queryset = queryset.filter(is_verified_provider=True)
            elif verified.lower() == 'false':
                queryset = queryset.filter(is_verified_provider=False)

        region = self.request.query_params.get('region')
        if region:
            queryset = queryset.filter(provider_profile__region__icontains=region)

        district = self.request.query_params.get('district')
        if district:
            queryset = queryset.filter(provider_profile__district__icontains=district)

        available = self.request.query_params.get('available')
        if available is not None:
            if available.lower() == 'true':
                queryset = queryset.filter(provider_profile__is_available=True)
            elif available.lower() == 'false':
                queryset = queryset.filter(provider_profile__is_available=False)

        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(average_rating__gte=min_rating)

        return queryset.order_by('-average_rating', '-reviews_count')