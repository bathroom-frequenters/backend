from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

import json

from .repositories import get_recent_and_latest_availability_as_serializable


class MonitorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(settings.ROOM_GROUP_NAME, self.channel_name)

        await self.accept()

        data: dict = get_recent_and_latest_availability_as_serializable()

        await self.send(text_data=json.dumps(data))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            settings.ROOM_GROUP_NAME, self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        if text_data == "SEND_DATA_PLZ_KTHXBAI":
            data = get_recent_and_latest_availability_as_serializable()

            await self.send(text_data=json.dumps(data))

    async def availability_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))
