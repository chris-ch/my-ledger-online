import logging
from django.contrib.auth.models import User
from rest_framework import serializers

from oas.models import Currency
from oas.models import LegalEntity


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

    #legal_entities = serializers.PrimaryKeyRelatedField(many=True, queryset=LegalEntity.objects.all())

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('code', 'name')
        #extra_kwargs = {
        #    'url': {
        #        'lookup_field': Currency.code
        #    }
        #}


class LegalEntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = LegalEntity
        fields = ('code', 'name', 'description', 'is_individual', 'owner', 'currency')

    #currency = CurrencySerializer(required=True, many=False)
    currency = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='code',
        queryset=Currency.objects.all()
     )
    owner = serializers.ReadOnlyField(source='owner.username')

    def create(self, validated_data):
        print('initial data: %s' % str(self.initial_data))
        print(dir(self))
        #serializer = CurrencySerializer(data=self.initial_data.get('currency'), many=False, read_only=True)
        #serializer.is_valid()
        #print('serial: %s' % str(serializer.errors))
        print('************ %s ************' % str(validated_data))
        currency = validated_data.get('currency')
        logging.error('currency: %s', currency)
        return LegalEntity.objects.create(**validated_data)

