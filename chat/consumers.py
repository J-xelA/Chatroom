from django.conf import settings
from .exceptions import ClientError
from .utils import get_room_or_error
from channels.generic.websocket import AsyncJsonWebsocketConsumer

"""
This chat consumer handles websocket connections for chat clients.
Chat consumer uses AsyncJsonWebsocketConsumer.
All the handling functions must be async functions.
http://channels.readthedocs.io/en/latest/topics/consumers.html
"""
class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket is handshaking for initial connection.
    """
    async def connect(self):
        # Is the user logged in?
        if self.scope["user"].is_anonymous:
            # Reject connection.
            await self.close()
        else:
            # Accept connection.
            await self.accept()
        # Store which room(s) the user joined on the connection.
        self.rooms = set()

    """
    WebSocket closing.
    """
    async def disconnect(self, code):
        for room_id in list(self.rooms):
            try:
                # Leave all the rooms you're connected to.
                await self.leave_room(room_id)
            except ClientError:
                pass

    """
    Django Channels will JSON-decode the payload to pass it as the first argument.
    """
    async def receive_json(self, content):
        # Messages have a command: join, leave, and send.
        command = content.get("command", None)
        try:
            if command == "join":
                # Join the room.
                await self.join_room(content["room"])
            elif command == "leave":
                # Leave the room.
                await self.leave_room(content["room"])
            elif command == "send":
                # Send message.
                await self.send_room(content["room"], content["message"])
        except ClientError as e:
            # Send JSON errors to console.
            await self.send_json({"error": e.code})


    """
    Called by receive_json when a user sends a join command.
    """
    async def join_room(self, room_id):
        # Logged-in user is in scope because of ASGI authentication.
        room = await get_room_or_error(room_id, self.scope["user"])
        # Send a join message if turned on.
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
            await self.channel_layer.group_send(room.group_name,
                {
                    "type": "chat.join",
                    "room_id": room_id,
                    "username": self.scope["user"].username,
                }
            )
        # Save that user is in a room.
        self.rooms.add(room_id)
        # Add to the group so users can receive messages.
        await self.channel_layer.group_add(
            room.group_name,
            self.channel_name,
        )
        # Tell client to finish opening the room.
        await self.send_json({
            "join": str(room.id),
            "title": room.title,
        })

    """
    Called by receive_json when a user sends a leave command.
    """
    async def leave_room(self, room_id):
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        room = await get_room_or_error(room_id, self.scope["user"])
        # Send a leave message if user leaves a room.
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
            await self.channel_layer.group_send(room.group_name,
                {
                    "type": "chat.leave",
                    "room_id": room_id,
                    "username": self.scope["user"].username,
                }
            )
        # Remove that user is in a room.
        self.rooms.discard(room_id)
        # User no longer receives messages.
        await self.channel_layer.group_discard(
            room.group_name,
            self.channel_name,
        )
        # Client closes the room.
        await self.send_json({
            "leave": str(room.id),
        })

    """
    Called by receive_json when a user sends a message to a room.
    """
    async def send_room(self, room_id, message):
        # Check if user is in a room.
        if room_id not in self.rooms:
            raise ClientError("ROOM_ACCESS_DENIED")
        # Get the room id and send to the group.
        room = await get_room_or_error(room_id, self.scope["user"])
        await self.channel_layer.group_send(room.group_name,
            {
                "type": "chat.message",
                "room_id": room_id,
                "username": self.scope["user"].username,
                "message": message,
            }
        )

    """
    Called when someone has joined the chat.
    """
    async def chat_join(self, event):
        # Send a message to the client.
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_ENTER,
                "room": event["room_id"],
                "username": event["username"],
            },
        )

    """
    Called when someone has left the chat.
    """
    async def chat_leave(self, event):
        # Send a message to the client.
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_LEAVE,
                "room": event["room_id"],
                "username": event["username"],
            },
        )

    """
    Called when someone has messaged the chat.
    """
    async def chat_message(self, event):
        # Send a message to the client.
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_MESSAGE,
                "room": event["room_id"],
                "username": event["username"],
                "message": event["message"],
            },
        )
