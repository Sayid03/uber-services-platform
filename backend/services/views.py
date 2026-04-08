from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework.exceptions import PermissionDenied

from .models import Category, Service
from .serializers import CategorySerializer, ServiceSerializer

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
        queryset = Service.objects.select_related('provider', 'category').all()

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_active=True)

        provider_id = self.request.query_params.get('provider')
        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)

        return queryset
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        user = self.request.user

        if user.role != 'provider':
            raise PermissionDenied('Only providers can create services.')

        serializer.save(provider=user)

class ServiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.select_related('provider', 'category').all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_update(self, serializer):
        service = self.get_object()
        user = self.request.user

        if service.provider != user:
            raise PermissionDenied('You can only update your own services.')

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        if instance.provider != user:
            raise PermissionDenied('You can only delete your own services.')

        instance.delete()
