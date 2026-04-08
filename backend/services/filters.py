import django_filters
from .models import Service

class ServiceFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')

    class Meta:
        model = Service
        fields = ['category', 'pricing_type', 'is_active', 'provider']