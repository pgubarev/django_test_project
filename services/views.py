from rest_framework import viewsets
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
)

import json

from services.consts import *
from services.models import Topic, Subscription
from services.serializers import (
    TopicSerializer,
    SubscriptionSerializer,
    SubscriptionCreateVerifier,
    SubscriptionConfirmVerifier,
    SubscriptionRequestVerifer
)
from services.utils import *


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class AddSubscribeView(ViewSet):

    def create(self, request, format=None):

        serializer = SubscriptionCreateVerifier(data=request.data)

        if serializer.is_valid(raise_exception=False):

            endpoint = serializer.validated_data['endpoint']
            protocol = PROTOCOL_HTTPS if endpoint.startswith(PROTOCOL_HTTPS) else PROTOCOL_HTTP
            serializer.validated_data['protocol'] = protocol

            sub = serializer.create(serializer.validated_data)
            sub.save()

            response_data = {
                'type': TYPE_SUB_CONFIRMATION,
                'message': MESSAGE_CREATED,
                'id': sub.id,
                'token': sub.token.__str__(),
                'subscription_url': 'http://localhost:8000/api/confirm/{0}/'.format(sub.id)
            }

            send_post_message.apply_async((sub.endpoint, response_data), countdown=10)

            return Response(json.dumps(response_data), status=HTTP_201_CREATED)

        response_data = json.dumps({'message': MESSAGE_INVALID_DATA})
        return Response(response_data, status=HTTP_400_BAD_REQUEST)


class ConfirmSubscribeView(ViewSet):

    def update(self, request, pk, format=None):

        serializer = SubscriptionConfirmVerifier(data=request.data)

        if serializer.is_valid(raise_exception=False):
            try:
                sub = Subscription.objects.get(id=pk, token=serializer.validated_data['token'])

                if sub.status == STATUS_CONFIRMED:
                    response_data = json.dumps({'message': MESSAGE_ALREADY_CONFIRMED})
                    return Response(response_data, status=HTTP_200_OK)

                if sub.status == STATUS_CANCELLED:
                    response_data = json.dumps({'message': MESSAGE_CANT_CONFIRM})
                    return Response(response_data, status=HTTP_200_OK)

                sub.status = STATUS_CONFIRMED
                sub.save()

                response_data = json.dumps({'message': MESSAGE_CONFIRMED})
                return Response(response_data, status=HTTP_200_OK)

            except Subscription.DoesNotExist:
                response_data = json.dumps({'message': MESSAGE_INVALID_DATA})
                return Response(response_data, status=HTTP_400_BAD_REQUEST)

        response_data = json.dumps({'message': MESSAGE_NOT_FOUND})
        return Response(response_data, status=HTTP_400_BAD_REQUEST)


class UnsubscribeView(ViewSet):

    def destroy(self, request, pk, format=None):
        try:
            sub = Subscription.objects.get(id=pk)
            sub.delete()
            response = json.dumps({'message': MESSAGE_DELETED})
            return Response(response, status=HTTP_204_NO_CONTENT)

        except Subscription.DoesNotExist:
            response = json.dumps({'message': MESSAGE_NOT_FOUND})
            return Response(response, status=HTTP_400_BAD_REQUEST)


class AutoConfirmSubscribeView(ViewSet):

    def create(self, request, format=None):

        serializer = SubscriptionRequestVerifer(data=request.data)

        if serializer.is_valid(raise_exception=False):

            url = serializer.validated_data['subscription_url']
            data = {
                'token': serializer.validated_data['token'].__str__(),
            }

            send_put_message.apply_async((url, data), countdown=10)

            return Response(status=HTTP_202_ACCEPTED)

        return Response(status=HTTP_400_BAD_REQUEST)
