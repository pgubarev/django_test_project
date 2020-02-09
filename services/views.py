from rest_framework import viewsets, mixins
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from services.consts import *
from services.models import Topic, Subscription
from services.serializers import (
    TopicSerializer,
    SubscriptionSerializer,
    SubCreateVerifySerializer,
    TokenVerifySerializer,
    SubRequestVerifySerializer
)
from services.utils import *


@permission_classes([IsAuthenticated])
class TopicViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(owner=user)


class SubscriptionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SubscriptionAPIView(viewsets.ViewSet):
    serializer_class = SubCreateVerifySerializer

    @action(detail=False, methods=['post'], url_path='subscribe',
            serializer_class=SubCreateVerifySerializer)
    def subscribe(self, request, format=None):

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            response_data = {'message': MESSAGE_INVALID_DATA}
            return Response(response_data, status=HTTP_400_BAD_REQUEST)

        endpoint = serializer.validated_data['endpoint']
        protocol = PROTOCOL_HTTPS if endpoint.startswith(PROTOCOL_HTTPS) else PROTOCOL_HTTP
        serializer.validated_data['protocol'] = protocol

        sub = serializer.save()

        response_data = {
            'type': TYPE_SUB_CONFIRMATION,
            'message': MESSAGE_CREATED,
            'id': sub.id,
            'token': str(sub.token),
            'subscription_url': self.reverse_action('confirm', args=[sub.id], request=request)
        }

        send_post_message.apply_async(args=(sub.endpoint, response_data), countdown=10)

        return Response(response_data, status=HTTP_201_CREATED)

    @action(detail=True, methods=['put'], url_path='confirm',
            serializer_class=TokenVerifySerializer)
    def confirm(self, request, pk, format=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            try:
                sub = Subscription.objects.get(id=pk, token=serializer.validated_data['token'])
            except Subscription.DoesNotExist:
                return Response({'message': MESSAGE_INVALID_DATA}, status=HTTP_400_BAD_REQUEST)

            if sub.status == STATUS_CONFIRMED:
                return Response({'message': MESSAGE_ALREADY_CONFIRMED})

            if sub.status == STATUS_CANCELLED:
                return Response({'message': MESSAGE_CANT_CONFIRM})

            sub.status = STATUS_CONFIRMED
            sub.save(update_fields=['status'])

            return Response({'message': MESSAGE_CONFIRMED})

        return Response({'message': MESSAGE_NOT_FOUND}, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='unsubscribe')
    def unsubscribe(self, request, pk, format=None):
        try:
            sub = Subscription.objects.get(id=pk)
        except Subscription.DoesNotExist:
            return Response({'message': MESSAGE_NOT_FOUND}, status=HTTP_400_BAD_REQUEST)

        sub.delete()
        return Response({'message': MESSAGE_DELETED}, status=HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='auto.confirm',
            serializer_class=SubRequestVerifySerializer)
    def auto_confirm(self, request, format=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            url = serializer.validated_data['subscription_url']
            data = {
                'token': str(serializer.validated_data['token']),
            }

            send_put_message.apply_async(args=(url, data), countdown=10)

            return Response(status=HTTP_202_ACCEPTED)

        return Response(status=HTTP_400_BAD_REQUEST)
