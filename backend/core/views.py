from rest_framework.response import Response
from rest_framework.views import APIView


class ApiRootView(APIView):
    def get(self, request):
        return Response({
            'users': '/api/users/',
            'services': '/api/services/',
            'bookings': '/api/bookings/',
            'reviews': '/api/reviews/',
        })