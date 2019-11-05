from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from services.views import (
    TopicViewSet,
    SubscriptionViewSet,
    AddSubscribeView,
    UnsubscribeView,
    ConfirmSubscribeView,
    AutoConfirmSubscribeView
)


router = DefaultRouter()
router.register('topics', TopicViewSet)
router.register('subscriptions', SubscriptionViewSet)
router.register('subscribe', AddSubscribeView, basename='subscribe')
router.register('confirm', ConfirmSubscribeView, basename='confirm')
router.register('unsubscribe', UnsubscribeView, basename='unsubscribe')
router.register('auto.confirm', AutoConfirmSubscribeView, basename='auto_confirm')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
