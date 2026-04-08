import django_filters
from .models import User

class ProviderFilter(django_filters.FilterSet):
    region = django_filters.CharFilter(field_name='provider_profile__region', lookup_expr='icontains')
    district = django_filters.CharFilter(field_name='provider_profile__district', lookup_expr='icontains')
    min_rating = django_filters.NumberFilter(method='filter_min_rating')

    class Meta:
        model = User
        fields = ['is_verified_provider']

    def filter_min_rating(self, queryset, name, value):
        return queryset.filter(average_rating__gte=value)