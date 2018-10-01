from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

from oas.models import Currency
from oas.models import LegalEntity
from oas.serializers import CurrencySerializer
from oas.serializers import LegalEntitySerializer


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


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def legal_entity_list(request, format=None):
    """
    Lists all legal entities or creates a new legal entity.
    """
    if request.method == 'GET':
        legal_entities = LegalEntity.objects.all()
        serializer = LegalEntitySerializer(legal_entities, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LegalEntitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes((permissions.AllowAny,))
def legal_entity_detail(request, code, format=None):
    """
    Retrieves, updates or deletes a legal entity.
    """
    try:
        legal_entity = LegalEntity.objects.get(code=code)
    except Currency.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LegalEntitySerializer(legal_entity)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LegalEntitySerializer(legal_entity, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        legal_entity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)