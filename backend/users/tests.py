from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, ProviderProfile

class UserAuthTests(APITestCase):
    def test_register_customer_success(self):
        url = reverse('register')
        data = {
            'username': 'customer1',
            'email': 'customer1@example.com',
            'password': 'strongpassword123',
            'confirm_password': 'strongpassword123',
            'first_name': 'Ali',
            'last_name': 'Karimov',
            'role': 'customer',
            'phone_number': '+998901112233'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().role, 'customer')
    
    def test_register_provider_creates_provider_profile(self):
        url = reverse('register')
        data = {
            'username': 'provider1',
            'email': 'provider1@example.com',
            'password': 'strongpassword123',
            'confirm_password': 'strongpassword123',
            'first_name': 'Bekzod',
            'last_name': 'Tursunov',
            'role': 'provider',
            'phone_number': '+998909998877'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='provider1')
        self.assertEqual(user.role, 'provider')
        self.assertTrue(ProviderProfile.objects.filter(user=user).exists())
    
    def test_register_fails_when_passwords_do_not_match(self):
        url = reverse('register')
        data = {
            'username': 'user1',
            'email': 'user1@example.com',
            'password': 'strongpassword123',
            'confirm_password': 'wrongpassword123',
            'role': 'customer'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        User.objects.create_user(
            username='testuser',
            password='strongpassword123',
            role='customer'
        )

        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'strongpassword123'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_me_requires_authentication(self):
        url = reverse('me')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_provider_list_returns_providers(self):
        url = reverse('provider-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
