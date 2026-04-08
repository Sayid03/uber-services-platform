from rest_framework import serializers
from .models import Category, Service

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon']

class ServiceSerializer(serializers.ModelSerializer):
    provider_username = serializers.CharField(source='provider.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.IntegerField(read_only=True)

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
            'average_rating',
            'reviews_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['provider', 'created_at', 'updated_at']
    
    def get_average_rating(self, obj):
        value = getattr(obj, 'average_rating', None)
        if value is None:
            return None
        return round(value, 2)

    def get_reviews_count(self, obj):
        return getattr(obj, 'reviews_count', 0)

    def validate(self, attrs):
        pricing_type = attrs.get('pricing_type', getattr(self.instance, 'pricing_type', None))
        price = attrs.get('price', getattr(self.instance, 'price', None))
        title = attrs.get('title', getattr(self.instance, 'title', None))
        description = attrs.get('description', getattr(self.instance, 'description', None))

        if not title or len(title.strip()) < 5:
            raise serializers.ValidationError({
                'title': 'Title must be at least 5 characters long.'
            })

        if not description or len(description.strip()) < 15:
            raise serializers.ValidationError({
                'description': 'Description must be at least 15 characters long.'
            })

        if pricing_type in ['fixed', 'hourly'] and price is None:
            raise serializers.ValidationError({
                'price': 'Price is required for fixed or hourly pricing.'
            })

        if price is not None and price < 0:
            raise serializers.ValidationError({
                'price': 'Price cannot be negative.'
            })

        return attrs
