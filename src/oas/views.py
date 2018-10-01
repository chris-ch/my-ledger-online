from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from oas.models import Currency
from oas.models import LegalEntity
from oas.serializers import CurrencySerializer
from oas.serializers import LegalEntitySerializer


@csrf_exempt
def currency_list(request):
    """
    Lists all currencies.
    """
    if request.method == 'GET':
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def currency_detail(request, code):
    """
    Retrieves a currency.
    """
    try:
        currency = Currency.objects.get(code=code)
    except Currency.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CurrencySerializer(currency)
        return JsonResponse(serializer.data)


@csrf_exempt
def legal_entity_list(request):
    """
    Lists all legal entities.
    """
    if request.method == 'GET':
        legal_entities = LegalEntity.objects.all()
        serializer = LegalEntitySerializer(legal_entities, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LegalEntitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def legal_entity_detail(request, code):
    """
    Retrieves, updates or deletes a legal entity.
    """
    try:
        legal_entity = LegalEntity.objects.get(code=code)
    except Currency.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = LegalEntitySerializer(legal_entity)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LegalEntitySerializer(legal_entity, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        legal_entity.delete()
        return HttpResponse(status=204)