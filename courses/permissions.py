from rest_framework.permissions import BasePermission

class OnlyAdminAndInstructor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user and user.is_staff:
            return True
        elif user and \
            user.role == user.INSTRUCTOR and \
            hasattr(request.user, 'instructor_profile'):
            return True
        return False