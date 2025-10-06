from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Room, Author, Message
from django.db import IntegrityError
from django.db.models import Count, Q



class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def Get_Room(self, room_id):
        try:
            room = Room.objects.get(pk=room_id)
            return room
        except Room.DoesNotExist:
            return None


    @database_sync_to_async
    def Get_Author(self, user):
        try:
            author = Author.objects.get(user = user)
            return author
        except Author.DoesNotExist:
            return None


    @database_sync_to_async
    def Save_Message(self, author, room, message):
        message_obj = Message.objects.create(
            author = author,
            room = room,
            context = message,
        )
        print(f"💾 Saved message #{message_obj.id}: {message_obj.context} by {author.author_name}")
        return message_obj


    async def chat_message(self, event):
        author_name = event['author_name']
        message = event['message']

        await self.send(text_data=json.dumps({
            'author_name': author_name,
            'message': message,
            'source': 'room_broadcast',
        }))



# MAIN:
    async def connect(self):
        print("✅ WebSocket client connected")
        #Lấy dữ liệu:
        data = self.scope['url_route']['kwargs']
        room_id = data.get('room_id')

        current_author = self.scope['user']
        if not current_author.is_authenticated:
            await self.close()
            return

        #Lấy phòng:
        room = await self.Get_Room(room_id)
        if room is None:
            await self.close()
            return

        #Thiết lập cho phòng
        self.room = room
        self.room_group_name = "chat_%d" % room.pk
        print(f"🏠 Connected to room: {self.room_group_name}")

        #Đăng kí phòng
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Kết nối WebSocket
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Kết nối thành công!"}))


    async def disconnect(self, close_code):
        # Ngắt kết nối
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        print("Client disconnected")


    async def receive(self, text_data):
        print(f"🔍 Receive running in room: {getattr(self, 'room_group_name', '❌ None')}")
    # Nhận message từ client
        data = json.loads(text_data)
        message = data.get("message", "")

        user = self.scope['user']
        if not user.is_authenticated:
            await self.close()
            return
        author = await self.Get_Author(user)

    # Chuẩn bị dữ liệu message thô:
        name = user.username 
        if author and author.author_name:
            name = author.author_name        
        
        message_data = {
            'type': "chat_message",
            'author_name': name,
            'message': message,
        }

    # Gửi message đến nhóm phòng chat
        await self.channel_layer.group_send(
            self.room_group_name,
            message_data,
        )

        await self.Save_Message(author, self.room, message)
        print(f"📩 Message received from {name}: {message} in room {self.room_group_name}")
        




