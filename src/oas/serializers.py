from rest_framework import serializers
from oas.models import Currency
from oas.models import LegalEntity


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('code', 'name')


class LegalEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalEntity
        fields = ('code', 'name', 'description', 'is_individual', 'currency')
