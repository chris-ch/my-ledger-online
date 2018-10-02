from django.contrib.auth.models import User
from rest_framework import serializers
from oas.models import Currency
from oas.models import LegalEntity


class UserSerializer(serializers.ModelSerializer):
    legal_entities = serializers.PrimaryKeyRelatedField(many=True, queryset=LegalEntity.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'legal_entities')


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('code', 'name')


class LegalEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalEntity
        fields = ('code', 'name', 'description', 'is_individual', 'currency', 'user')

    user = serializers.ReadOnlyField(source='user.username')
