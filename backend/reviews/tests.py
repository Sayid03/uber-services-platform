from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from services.models import Category, Service
from bookings.models import Booking
from .models import Review

class ReviewTests(APITestCase):
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
            status='completed'
        )
    
    def test_customer_can_create_review_for_completed_booking(self):
        self.client.force_authenticate(user=self.customer)
        url = reverse('review-list-create')

        data = {
            'booking': self.booking.id,
            'rating': 5,
            'comment': 'Excellent and professional service.'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
    
    def test_cannot_review_same_booking_twice(self):
        Review.objects.create(
            booking=self.booking,
            customer=self.customer,
            provider=self.provider,
            service=self.service,
            rating=5,
            comment='First review'
        )

        self.client.force_authenticate(user=self.customer)
        url = reverse('review-list-create')

        data = {
            'booking': self.booking.id,
            'rating': 4,
            'comment': 'Second review attempt'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_cannot_review_incomplete_booking(self):
        pending_booking = Booking.objects.create(
            customer=self.customer,
            provider=self.provider,
            service=self.service,
            booking_date='2026-04-21T14:00:00Z',
            address='Chilanzar, Tashkent',
            estimated_price=150000,
            status='pending'
        )

        self.client.force_authenticate(user=self.customer)
        url = reverse('review-list-create')

        data = {
            'booking': pending_booking.id,
            'rating': 4,
            'comment': 'Should fail'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_cannot_review_incomplete_booking(self):
        pending_booking = Booking.objects.create(
            customer=self.customer,
            provider=self.provider,
            service=self.service,
            booking_date='2026-04-21T14:00:00Z',
            address='Chilanzar, Tashkent',
            estimated_price=150000,
            status='pending'
        )

        self.client.force_authenticate(user=self.customer)
        url = reverse('review-list-create')

        data = {
            'booking': pending_booking.id,
            'rating': 4,
            'comment': 'Should fail'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
