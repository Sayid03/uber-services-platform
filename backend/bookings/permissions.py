from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'customer'
    
class IsProvider(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'provider'
    
class IsBookingParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and
            (obj.customer == request.user or obj.provider == request.user)
        )

class IsBookingProvider(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.provider == request.user