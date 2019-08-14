from rest_framework import serializers

from .repositories import create_availability
from .signals import AvailabilityUpdate


class SensorUploadSerializer(serializers.Serializer):
    available = serializers.BooleanField(write_only=True, required=True)

    def create(self, validated_data) -> bool:
        result = create_availability(validated_data["available"])

        AvailabilityUpdate.send(sender=self.__class__)

        return result


class SensorStatusSerializer(serializers.Serializer):
    available = serializers.BooleanField(allow_null=True)
    time = serializers.CharField()
