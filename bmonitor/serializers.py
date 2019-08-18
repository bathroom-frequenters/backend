from django.conf import settings
from rest_framework import serializers

from .repositories import create_availability
from .signals import AvailabilityUpdate


class SensorUploadSerializer(serializers.Serializer):
    available = serializers.BooleanField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, val):
        if val != settings.API_PASSWORD:
            raise serializers.ValidationError("Incorrect password")

        return val

    def create(self, validated_data) -> bool:
        result = create_availability(validated_data["available"])

        AvailabilityUpdate.send(sender=self.__class__)

        return result


class SensorStatusSerializer(serializers.Serializer):
    available = serializers.BooleanField(allow_null=True)
    time = serializers.CharField()
