from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TicketEntry(models.Model):
    description = models.CharField(max_length=128)
    entry = models.CharField(max_length=65536)
    status = models.BooleanField(default=False)
    name = models.CharField(max_length=128, default="anon")
