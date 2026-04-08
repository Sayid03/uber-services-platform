from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(source='customer.username', read_only=True)
    provider_username = serializers.CharField(source='provider.username', read_only=True)
    service_title = serializers.CharField(source='service.title', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'customer',
            'customer_username',
            'provider',
            'provider_username',
            'service',
            'service_title',
            'booking_date',
            'address',
            'notes',
            'estimated_price',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'customer',
            'provider',
            'status',
            'created_at',
            'updated_at',
        ]
    
    def validate(self, attrs):
        service = attrs.get('service')
        request = self.context.get('request')

        if service and not service.is_active:
            raise serializers.ValidationError({
                'service': 'Inactive services cannot be booked.'
            })

        if request and request.user == service.provider:
            raise serializers.ValidationError({
                'service': 'You cannot book your own service.'
            })

        return attrs
    
class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['status']

    def validate_status(self, value):
        allowed_statuses = [
            'accepted',
            'in_progress',
            'completed',
            'cancelled',
        ]
        if value not in allowed_statuses:
            raise serializers.ValidationError('Invalid status update.')
        return value