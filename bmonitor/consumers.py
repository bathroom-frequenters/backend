from channels.generic.websocket import AsyncWebsocketConsumer
import json


ROOM_GROUP_NAME = "Alexandria"


class MonitorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(ROOM_GROUP_NAME, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(ROOM_GROUP_NAME, self.channel_name)

    async def availability_update(self, event):

        await self.send(text_data=json.dumps({"available": True, "time": None}))
