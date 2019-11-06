from django.core.validators import URLValidator
from rest_framework import serializers

from services.models import Topic, Subscription
from services.consts import TYPE_SUB_CONFIRMATION


class TopicSerializer(serializers.ModelSerializer):

    email = serializers.CharField(source='owner.email', read_only=True)

    class Meta:
        fields = ['topic', 'email']
        model = Topic


class SubscriptionSerializer(serializers.ModelSerializer):

    topic = serializers.CharField(source='topic.topic', read_only=True)

    class Meta:
        fields = ['token', 'topic', 'protocol', 'endpoint', 'status', 'created_timestamp']
        model = Subscription


class TokenVerifySerializer(serializers.Serializer):
    token = serializers.UUIDField(format='hex_verbose')


class SubCreateVerifySerializer(serializers.ModelSerializer):

    endpoint = serializers.URLField(
        allow_blank=False,
        allow_null=False,
        validators=[
            URLValidator(schemes=['http', 'https'])
        ]
    )

    class Meta:
        model = Subscription
        fields = ['topic', 'endpoint']


class SubRequestVerifySerializer(serializers.Serializer):
    token = serializers.UUIDField(format='hex_verbose')
    subscription_url = serializers.URLField()
    type = serializers.ChoiceField(choices=[TYPE_SUB_CONFIRMATION,])
