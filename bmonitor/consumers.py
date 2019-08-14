from channels.generic.websocket import AsyncWebsocketConsumer
from dataclasses import asdict
from django.conf import settings
from typing import List

import json

from .entities import AvailabilityRecord
from .repositories import get_recent_availability


class MonitorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(settings.ROOM_GROUP_NAME, self.channel_name)

        await self.accept()

        records: List[AvailabilityRecord] = get_recent_availability()
        data: List[dict] = list(map(asdict, records))

        await self.send(text_data=json.dumps(data))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            settings.ROOM_GROUP_NAME, self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        if text_data == "SEND_DATA_PLZ_KTHXBAI":
            records: List[AvailabilityRecord] = get_recent_availability()
            data: List[dict] = list(map(asdict, records))

            await self.send(text_data=json.dumps(data))

    async def availability_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))
