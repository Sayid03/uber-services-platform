from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import ApiRootView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', ApiRootView.as_view(), name='api-root'),
    path('api/users/', include('users.urls')),
    path('api/services', include('services.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('api/reviews/', include('reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)