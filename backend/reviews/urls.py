from django.urls import path
from .views import ReviewListCreateAPIView, ReviewDetailAPIView

urlpatterns = [
    path('', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),
]
