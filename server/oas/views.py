import logging
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from oas.models import Currency
from oas.models import LegalEntity

from oas.serializers import UserSerializer
from oas.serializers import CurrencySerializer
from oas.serializers import LegalEntitySerializer


@permission_classes((permissions.IsAdminUser,))
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@permission_classes((permissions.IsAdminUser,))
class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class LegalEntityList(generics.ListCreateAPIView):
    queryset = LegalEntity.objects.all()
    serializer_class = LegalEntitySerializer

    def perform_create(self, serializer):
        print('###### TEST %s ######' % str(self.request.data))
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)


@permission_classes((permissions.IsAdminUser,))
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

