from django.conf import settings
from django.core.validators import URLValidator
from django.db import models
import uuid

from services.consts import *


class Topic(models.Model):
    topic = models.CharField(max_length=40, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic


class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    protocol = models.CharField(max_length=5, default='http', null=False, choices=[
        (PROTOCOL_HTTP, PROTOCOL_HTTP),
        (PROTOCOL_HTTPS, PROTOCOL_HTTPS)
    ])
    status = models.CharField(max_length=10, default='pending', null=False, choices=[
        (STATUS_PENDING, STATUS_PENDING),
        (STATUS_CANCELLED, STATUS_CANCELLED),
        (STATUS_CONFIRMED, STATUS_CONFIRMED)
    ])
    endpoint = models.URLField(null=False, validators=[URLValidator(
        schemes=['http', 'https']
    )])
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token.__str__()
