from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import Category, Service

class ServiceTests(APITestCase):
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
        self.other_provider = User.objects.create_user(
            username='provider2',
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
    
    def test_provider_can_create_service(self):
        self.client.force_authenticate(user=self.provider)
        url = reverse('service-list-create')

        data = {
            'category': self.category.id,
            'title': 'Sink Repair',
            'description': 'Professional sink repair for homes.',
            'pricing_type': 'fixed',
            'price': 100000,
            'location': 'Tashkent',
            'is_active': True
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Service.objects.count(), 2)
    
    def test_customer_cannot_create_service(self):
        self.client.force_authenticate(user=self.customer)
        url = reverse('service-list-create')

        data = {
            'category': self.category.id,
            'title': 'Invalid Service',
            'description': 'This should not be allowed.',
            'pricing_type': 'fixed',
            'price': 50000,
            'location': 'Tashkent',
            'is_active': True
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_only_owner_can_update_service(self):
        self.client.force_authenticate(user=self.other_provider)
        url = reverse('service-detail', kwargs={'pk': self.service.id})

        response = self.client.patch(url, {'title': 'Updated Title'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_public_users_only_see_active_services(self):
        self.service.is_active = False
        self.service.save()

        url = reverse('service-list-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
