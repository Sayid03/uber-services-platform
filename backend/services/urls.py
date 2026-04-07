from django.urls import path
from .views import (
    CategoryListAPIView,
    ServiceListCreateAPIView,
    ServiceDetailAPIView,
)

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('', ServiceListCreateAPIView.as_view(), name='service-list-create'),
    path('<int:pk>/', ServiceDetailAPIView.as_view(), name='service-detail'),
]