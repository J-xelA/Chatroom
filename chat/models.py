from django.db import models


"""
Chat room model.
"""
class Room(models.Model):
    title = models.CharField(max_length=255)
    # Only admin users allowed (staff on django's user)
    staff_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    """
    Returns Channels Group name that websockets
    subscribe to for sending messages.
    """
    @property
    def group_name(self):
        return "room-%s" % self.id
