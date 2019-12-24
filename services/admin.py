from django.contrib import admin

from services.models import Topic, Subscription
from services.consts import PROTOCOL_HTTP, PROTOCOL_HTTPS


class TopicAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields = ('id', 'topic',)

    def save_model(self, request, obj, form, change):
        if obj.owner_id is None:
            obj.owner = request.user
        super().save_model(request, obj, form, change)


class SubscriptionAdmin(admin.ModelAdmin):
    exclude = ('token', 'protocol', 'created_timestamp',)

    def save_model(self, request, obj, form, change):
        obj.protocol = PROTOCOL_HTTPS if obj.endpoint.startswith(PROTOCOL_HTTPS) else PROTOCOL_HTTP
        super.save_model(request, obj, form, change)


admin.site.register(Topic, TopicAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
