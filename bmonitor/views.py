from dataclasses import asdict
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from typing import List

from .entities import AvailabilityRecord
from .repositories import get_latest_availability, get_recent_availability
from .serializers import SensorUploadSerializer, SensorStatusSerializer


class SensorUploadViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    serializer_class = SensorUploadSerializer


class SensorStatusViewSet(viewsets.GenericViewSet):
    serializer_class = SensorStatusSerializer

    @action(methods=["GET"], detail=False)
    def current(self, request):
        current: AvailabilityRecord = get_latest_availability()

        data: dict = asdict(current)

        serializer = SensorStatusSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def recent(self, request):
        recent: List[AvailabilityRecord] = get_recent_availability()

        data: List[dict] = list(map(asdict, recent))

        serializer = SensorStatusSerializer(data=data, many=True)

        serializer.is_valid(raise_exception=True)

        return Response({"results": serializer.data}, status=status.HTTP_200_OK)
