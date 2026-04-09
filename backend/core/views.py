from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView


@extend_schema(exclude=True)
class ApiRootView(APIView):
    def get(self, request):
        return Response({
            'users': '/api/users/',
            'services': '/api/services/',
            'bookings': '/api/bookings/',
            'reviews': '/api/reviews/',
        })