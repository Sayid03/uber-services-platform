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
        booking_date = attrs.get('booking_date')
        address = attrs.get('address')

        if not service:
            raise serializers.ValidationError({'service': 'Service is required.'})

        if not service.is_active:
            raise serializers.ValidationError({'service': 'Inactive services cannot be booked.'})

        if request and request.user == service.provider:
            raise serializers.ValidationError({'service': 'You cannot book your own service.'})

        if booking_date is None:
            raise serializers.ValidationError({'booking_date': 'Booking date is required.'})

        if not address or len(address.strip()) < 5:
            raise serializers.ValidationError({'address': 'Address must be at least 5 characters long.'})

        return attrs
    
class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['status']

    def validate(self, attrs):
        booking = self.instance
        new_status = attrs.get('status')

        allowed_transitions = {
            'pending': ['accepted', 'cancelled'],
            'accepted': ['in_progress', 'cancelled'],
            'in_progress': ['completed'],
            'completed': [],
            'cancelled': [],
        }

        current_status = booking.status
        allowed_next = allowed_transitions.get(current_status, [])

        if new_status not in allowed_next:
            raise serializers.ValidationError({
                'status': f'Cannot change status from "{current_status}" to "{new_status}".'
            })

        return attrs