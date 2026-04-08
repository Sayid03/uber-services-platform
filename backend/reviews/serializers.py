from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(source='customer.username', read_only=True)
    provider_username = serializers.CharField(source='provider.username', read_only=True)
    service_title = serializers.CharField(source='service.title', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'booking',
            'customer',
            'customer_username',
            'provider',
            'provider_username',
            'service',
            'service_title',
            'rating',
            'comment',
            'created_at',
        ]
        read_only_fields = [
            'customer',
            'provider',
            'service',
            'created_at',
        ]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value
    
    def validate(self, attrs):
        request = self.context.get('request')
        booking = attrs.get('booking')

        if not booking:
            raise serializers.ValidationError({'booking': 'Booking is required.'})

        if booking.status != 'completed':
            raise serializers.ValidationError({
                'booking': 'You can only review completed bookings.'
            })

        if booking.customer != request.user:
            raise serializers.ValidationError({
                'booking': 'You can only review your own completed bookings.'
            })

        if hasattr(booking, 'review'):
            raise serializers.ValidationError({
                'booking': 'This booking already has a review.'
            })

        return attrs