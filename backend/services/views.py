from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework.exceptions import PermissionDenied

from .models import Category, Service
from .serializers import CategorySerializer, ServiceSerializer
from .permissions import IsProvider, IsServiceOwnerOrReadOnly

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class ServiceListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'pricing_type', 'is_active']
    search_fields = ['title', 'description', 'location', 'provider__username']
    ordering_fields = ['created_at', 'price', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Service.objects.select_related('provider', 'category')

        if self.request.user.is_authenticated and self.request.user.role == 'provider':
            queryset = queryset.filter(Q(is_active=True) | Q(provider=self.request.user))
        else:
            queryset = queryset.filter(is_active=True)

        provider_id = self.request.query_params.get('provider')
        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)

        return queryset
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsProvider()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)

class ServiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsServiceOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        queryset = Service.objects.select_related('provider', 'category')

        if user.is_authenticated and user.role == 'provider':
            return queryset.filter(Q(is_active=True) | Q(provider=user))

        return queryset.filter(is_active=True)
