from rest_framework import serializers
from .models import Category, Service

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon']

class ServiceSerializer(serializers.ModelSerializer):
    provider_username = serializers.CharField(source='provider.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Service
        fields = [
            'id',
            'provider',
            'provider_username',
            'category',
            'category_name',
            'title',
            'description',
            'pricing_type',
            'price',
            'estimated_duration_hours',
            'location',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['provider', 'created_at', 'updated_at']

    def validate(self, attrs):
        pricing_type = attrs.get('pricing_type', getattr(self.instance, 'pricing_type', None))
        price = attrs.get('price', getattr(self.instance, 'price', None))

        if pricing_type in ['fixed', 'hourly'] and price is None:
            raise serializers.ValidationError({
                'price': 'Price is required for fixed or hourly pricing.'
            })

        return attrs