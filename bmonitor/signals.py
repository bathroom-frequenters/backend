from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from dataclasses import asdict
from django.conf import settings
from django.dispatch import Signal
from typing import List

from .entities import AvailabilityRecord
from .repositories import get_recent_availability

AvailabilityUpdate = Signal()


def broadcast_availability_update(sender, **kwargs):
    layer = get_channel_layer()

    records: List[AvailabilityRecord] = get_recent_availability()
    data: List[dict] = list(map(asdict, records))

    async_to_sync(layer.group_send)(
        settings.ROOM_GROUP_NAME, {"type": "availability.update", "data": data}
    )
