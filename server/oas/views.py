import logging
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from oas.models import Currency
from oas.models import LegalEntity

from oas.serializers import UserSerializer
from oas.serializers import CurrencySerializer
from oas.serializers import LegalEntitySerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        logging.info('checking permissions')
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


@permission_classes((permissions.IsAdminUser,))
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@permission_classes((permissions.IsAdminUser,))
class UserDetail(generics.RetrieveUpdateAPIView):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    #def get_object(self):
    #    username = self.kwargs["username"]
    #    return get_object_or_404(User, username=username)
#
    #def put(self, request, *args, **kwargs):
    #    return self.update(request, *args, **kwargs)


@permission_classes((permissions.IsAuthenticated,))
class LegalEntityList(generics.ListCreateAPIView):
    queryset = LegalEntity.objects.all()
    serializer_class = LegalEntitySerializer

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        logging.info('*** CHECKING ***')
        return self.list(request, *args, **kwargs)


@permission_classes((IsOwnerOrReadOnly,))
class LegalEntityDetail(generics.RetrieveUpdateAPIView):
    queryset = LegalEntity.objects.all()
    serializer_class = LegalEntitySerializer


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class CurrencyList(generics.ListCreateAPIView):
    lookup_field = Currency.code
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class CurrencyDetail(generics.RetrieveUpdateAPIView):
    lookup_field = Currency.code
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

