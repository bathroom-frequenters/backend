from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.dispatch import Signal

from .repositories import get_recent_and_latest_availability_as_serializable

AvailabilityUpdate = Signal()


def broadcast_availability_update(sender, **kwargs):
    layer = get_channel_layer()

    data: dict = get_recent_and_latest_availability_as_serializable()

    async_to_sync(layer.group_send)(
        settings.ROOM_GROUP_NAME, {"type": "availability.update", "data": data}
    )
