from django.contrib import admin
from . import models
from accounts.models import Account
# from events.forms import AccountManageForm
from senders.models import Sender


@admin.register(models.EventReceiver)
class EventReceiverAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sender',
        'receiver',
        'event_display',
        'opened',
        'clicked',
        'created_at',
        'updated_at'
    )

    list_display_links = (
        'id',
        'sender',
        'receiver',
        'event_display'
    )

    list_per_page = 50

    readonly_fields = ["opened", "clicked"]

    def sender(self, obj):
        return obj.event.sender.email

    def receiver(self, obj):
        return obj.account.email
    
    def event_display(self, obj):
        return "{start} - {end} \n{summary}".format(
            start=obj.event.start,
            end=obj.event.end,
            summary=obj.event.summary
        )
