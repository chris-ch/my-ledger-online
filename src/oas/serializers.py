from rest_framework import serializers
from oas.models import Currency


class CurrencySerializer(serializers.Serializer):
    code = serializers.CharField(required=True, allow_blank=False, max_length=9)
    name = serializers.CharField(required=True, allow_blank=False)

    def create(self, validated_data):
        """
        Create and return a new `Currency` instance, given the validated data.
        """
        return Currency.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Currency` instance, given the validated data.
        """
        instance.code = validated_data.get('code', instance.code)
        instance.title = validated_data.get('name', instance.name)
        instance.save()
        return instance