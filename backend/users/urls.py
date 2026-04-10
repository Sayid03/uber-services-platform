from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView, MeView, ProviderProfileUpdateView, ProviderListAPIView, ProviderDetailAPIView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('provider-profile/', ProviderProfileUpdateView.as_view(), name='provider-profile'),
    path('providers/', ProviderListAPIView.as_view(), name='provider-list'),
    path('providers/<int:id>/', ProviderDetailAPIView.as_view(), name='provider-detail'),
]