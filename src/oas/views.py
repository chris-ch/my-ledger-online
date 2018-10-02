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
        serializer.save(user=self.request.user)


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class LegalEntityDetail(generics.RetrieveUpdateAPIView):
    queryset = LegalEntity.objects.all()
    serializer_class = LegalEntitySerializer


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def currency_list(request, format=None):
    """
    Lists all currencies.
    """
    if request.method == 'GET':
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def currency_detail(request, code, format=None):
    """
    Retrieves a currency.
    """
    try:
        currency = Currency.objects.get(code=code)
    except Currency.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = CurrencySerializer(currency)
        return Response(serializer.data)
