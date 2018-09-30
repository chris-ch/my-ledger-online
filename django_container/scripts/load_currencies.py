from oas import models


def run(*args):
    currencies = models.Currency.objects.all()
    print('currencies: ' + str(currencies))
