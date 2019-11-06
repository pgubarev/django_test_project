from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from services.views import (
    TopicViewSet,
    SubscriptionViewSet,
    SubscriptionAPIView,
)


router = DefaultRouter()
router.register('trace/topics', TopicViewSet)
router.register('trace/subscriptions', SubscriptionViewSet)
router.register('subscriptions', SubscriptionAPIView, basename='subscriptions')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
