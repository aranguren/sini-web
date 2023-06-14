from rest_framework import permissions
import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

class IsWorkerAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        #authorization = request.META.get("HTTP_AUTHORIZATION")
        #token = authorization.split(" ")[1]
        print(request)
        #return True
        if not isinstance(request.user, AnonymousUser):
            return bool(request.user)
        return False

class IsWorkerRegistered(permissions.BasePermission):
    """
    Allows access only to registered workers.
    """
    def has_permission(self, request, view):
        if not isinstance(request.user, AnonymousUser):
            return bool(request.user and request.user.is_registered)
        return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.reported_by == request.user

class IsFreshToken(permissions.BasePermission):

    def has_permission(self, request, view):
        
        authorization = request.META.get("HTTP_AUTHORIZATION")
        token = authorization.split(" ")[1]
        print(authorization)
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
                
        if request.auth.token_type == 'access':
            return True
        else:
            return False

class IsWorkerMessage(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.worker == request.user

class IsWorkerDevice(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.id == request.user.id

