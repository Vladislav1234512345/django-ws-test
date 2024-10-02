# chat/consumers.py
import json
from django.utils import timezone

from channels.db import database_sync_to_async

from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Chat, Message, ChatUsers


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Получение пользователя
        user = self.scope["user"]

        # Получение чата по id
        chat = await database_sync_to_async(Chat.objects.get)(pk=self.chat_id)

        # Обновление поля "last_seen" экземпляра чата данного пользователя
        await self.update_chat_user(user=user, chat=chat)

        await self.accept()

    async def disconnect(self, close_code):
        # Получение пользователя
        user = self.scope["user"]

        # Получение чата по id
        chat = await database_sync_to_async(Chat.objects.get)(pk=self.chat_id)

        # Обновление поля "last_seen" перед выходом
        await self.update_chat_user(user=user, chat=chat)
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json["message"]

        # получить отправителя
        user = self.scope["user"]

        # Получение чата по id
        chat = await database_sync_to_async(Chat.objects.get)(pk=self.chat_id)

        # создание экземпляра сообщения
        message = await database_sync_to_async(Message.objects.create)(
            chat=chat,
            sender=user,
            text=text,
        )

        # Обновление поля "last_seen" экземпляра чата данного пользователя
        await self.update_chat_user(user=user, chat=chat)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": text}
        )

    #Декоратор для базы данных из синхронности в асинхронность
    @database_sync_to_async
    # Обновление chat_user
    def update_chat_user(self, chat, user):
        # Находим запись для chat и user
        chat_user = ChatUsers.objects.get(chat=chat, user=user)
        # Обновляем поле date_joined
        chat_user.last_seen = timezone.now()
        # Сохраняем экземпляр
        chat_user.save()


    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))