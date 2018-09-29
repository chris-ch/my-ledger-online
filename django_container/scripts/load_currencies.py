from oas import models


def run(*args):
    print('**PING** {}'.format(str(args)))
    return models.Currency.objects.all()
