from rest_framework.permissions import BasePermission
from django.conf import settings


class MenuManager(BasePermission):
    message = 'This action is allowed only for a manager.'

    def has_permission(self, request, view):
        token = request.META.get('HTTP_X_ACCESS_TOKEN')
        return token and token == settings.ACCESS_TOKEN
