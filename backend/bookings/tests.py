from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from services.models import Category, Service
from .models import Booking

class BookingTests(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username='customer1',
            password='strongpassword123',
            role='customer'
        )
        self.provider = User.objects.create_user(
            username='provider1',
            password='strongpassword123',
            role='provider'
        )

        self.category = Category.objects.create(
            name='Plumber',
            slug='plumber'
        )

        self.service = Service.objects.create(
            provider=self.provider,
            category=self.category,
            title='Pipe Leak Repair',
            description='Fast repair of leaking pipes in apartments.',
            pricing_type='fixed',
            price=150000,
            location='Tashkent',
            is_active=True
        )

        self.booking = Booking.objects.create(
            customer=self.customer,
            provider=self.provider,
            service=self.service,
            booking_date='2026-04-20T14:00:00Z',
            address='Yunusabad, Tashkent',
            estimated_price=150000,
            status='pending'
        )
    
    def test_customer_can_create_booking(self):
        self.client.force_authenticate(user=self.customer)
        url = reverse('booking-list-create')

        data = {
            'service': self.service.id,
            'booking_date': '2026-04-21T10:00:00Z',
            'address': 'Chilanzar, Tashkent',
            'notes': 'Please arrive before noon'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)

    def test_provider_cannot_create_booking(self):
        self.client.force_authenticate(user=self.provider)
        url = reverse('booking-list-create')

        data = {
            'service': self.service.id,
            'booking_date': '2026-04-21T10:00:00Z',
            'address': 'Chilanzar, Tashkent'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_customer_cannot_book_own_service(self):
        own_provider = User.objects.create_user(
            username='provider_customer',
            password='strongpassword123',
            role='provider'
        )
        own_service = Service.objects.create(
            provider=own_provider,
            category=self.category,
            title='Own Service',
            description='This is own service test description.',
            pricing_type='fixed',
            price=100000,
            location='Tashkent',
            is_active=True
        )

        self.client.force_authenticate(user=own_provider)
        url = reverse('booking-list-create')

        data = {
            'service': own_service.id,
            'booking_date': '2026-04-21T10:00:00Z',
            'address': 'Tashkent'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_provider_can_update_booking_status_with_valid_transition(self):
        self.client.force_authenticate(user=self.provider)
        url = reverse('booking-status-update', kwargs={'pk': self.booking.id})

        response = self.client.patch(url, {'status': 'accepted'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'accepted')

    def test_invalid_booking_status_transition_fails(self):
        self.client.force_authenticate(user=self.provider)
        url = reverse('booking-status-update', kwargs={'pk': self.booking.id})

        response = self.client.patch(url, {'status': 'completed'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_booking_participants_can_view_booking(self):
        stranger = User.objects.create_user(
            username='stranger',
            password='strongpassword123',
            role='customer'
        )
        self.client.force_authenticate(user=stranger)

        url = reverse('booking-detail', kwargs={'pk': self.booking.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
