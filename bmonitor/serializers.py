from rest_framework import serializers

from .repositories import create_availability


class SensorUploadSerializer(serializers.Serializer):
    available = serializers.BooleanField(write_only=True, required=True)

    def create(self, validated_data) -> bool:
        return create_availability(validated_data["available"])


class SensorStatusSerializer(serializers.Serializer):
    available = serializers.BooleanField(allow_null=True)
    time = serializers.CharField()
