import asyncio
import base64
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from utils.auth import get_user_id
from llm.assistant import create_manager, AssistantManager
from llm.utils import tts
from typing import Dict
from channels.db import database_sync_to_async
from chat.models import ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):

    managers: Dict[str, AssistantManager] = {}

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        # user_id = get_user_id(self.scope["query_string"].decode("utf-8"))

        # if not user_id:
        #     await self.close()
        #     return

        # if user_id != self.room_name:
        #     await self.close()
        #     return

        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name)

        # Create assistant manager
        if self.room_name not in self.managers:
            manager = create_manager()
            self.managers[self.room_name] = manager

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name)

    def get_manager(self):
        return self.managers[self.room_name]

    @database_sync_to_async
    def add_chat_message(self, message, ai=False):
        ChatMessage.objects.create(
            room_name=self.room_name,
            message=message,
            ai=ai
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Pass message to assistant
        manager = self.managers[self.room_name]
        transcript = message

        # Add message to database
        await self.add_chat_message(message)

        print(message)

        run = manager.run_assistant(transcript)

        # Add message to database
        await self.add_chat_message(run, ai=True)

        # Send message to room group
        await self.send(text_data=json.dumps({"message": run}))

        await asyncio.sleep(1)

        print("Started TTS")
        # Convert response to audio
        response = tts(run)
        print("Finished TTS")

        for chunk in response.iter_bytes():
            print("Sending chunk")
            await self.send(bytes_data=chunk)
            # await asyncio.sleep(1)

    # Receive message from room group

    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
