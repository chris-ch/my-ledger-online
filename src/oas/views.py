from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from oas.models import Currency
from oas.serializers import CurrencySerializer


@csrf_exempt
def currency_list(request):
    """
    List all currencies.
    """
    if request.method == 'GET':
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def currency_detail(request, code):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        currency = Currency.objects.get(code=code)
    except Currency.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CurrencySerializer(currency)
        return JsonResponse(serializer.data)
