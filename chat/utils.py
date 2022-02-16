from channels.db import database_sync_to_async
from .exceptions import ClientError
from .models import Room

# http://channels.readthedocs.io/en/latest/topics/databases.html
"""
Fetch a room for the user and check permissions.
"""
@database_sync_to_async
def get_room_or_error(room_id, user):
    # Is user logged in?
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    # Find requested room by id.
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise ClientError("ROOM_INVALID")
    # Check admin permissions.
    if room.staff_only and not user.is_staff:
        raise ClientError("ROOM_ACCESS_DENIED")
    return room
