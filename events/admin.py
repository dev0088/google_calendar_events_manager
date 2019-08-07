from django.contrib import admin
import nested_admin
import json
from . import models
from django.utils.timezone import get_current_timezone
from django.core.serializers.json import DjangoJSONEncoder
from . import google_calendar
from accounts.models import Account
from event_receivers.models import EventReceiver
from .serializers import EventSerializer, ReminderSerializer, OverrideSerializer
from django.core import serializers
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser


class OverrideInline(nested_admin.NestedStackedInline):
    model = models.Override
    extra = 0
    fields = [('method', 'minutes')]


class ReminderInline(nested_admin.NestedStackedInline):
    model = models.Reminder
    extra = 0
    inlines = [OverrideInline]


@admin.register(models.Event)
class EventAdmin(nested_admin.NestedModelAdmin):
    list_display = (
        'id',
        'sender_display',
        'summary',
        'description',
        'start',
        'end',
        'accounts_display',
        'created_at',
        'updated_at'
    )
    list_display_links = (
        'id',
        'sender_display',
        'summary',
        'description',
        'start',
        'end',
    )
    list_per_page = 50

    fields = ['sender', 'summary', 'description', ('start', 'end', ), 'accounts',]
    readonly_fields = ['calendar_id']
    filter_horizontal = ('accounts',)

    def sender_display(self, obj):
        return obj.sender.email

    def accounts_display(self, obj):
        return ", ".join([
            account.email for account in obj.accounts.all()
        ])

    sender_display.short_description = "Sender"
    accounts_display.short_description = "Accounts"

    inlines = [ReminderInline,]

    def save_model(self, request, obj, form, change):
        # Send add_event request to google
        event = {
            'summary': obj.summary,
            'location': obj.sender.last_location,
            'description': obj.description,
            'start': {
                'dateTime': obj.start.isoformat(),
                'timeZone': get_current_timezone().tzname(None)
            },
            'end': {
                'dateTime': obj.end.isoformat(), #'2019-08-04T17:00:00-07:00',
                'timeZone': get_current_timezone().tzname(None) #'America/Los_Angeles',
            },
            'attendees': [{'email': account.email} for account in form.cleaned_data['accounts']],
            'reminders': json.loads(json.dumps(ReminderSerializer(obj.event_reminder).data))
        }
        print('====== event: ', event)
        google_calendar_event = google_calendar.add_event(
            event, 
            obj.sender.google_oauth2_client_id, 
            obj.sender.google_oauth2_secrete
        )

        obj.calendar_id = google_calendar_event.get('id')
        super().save_model(request, obj, form, change)

        # Add EventReceivers for each account matching to this event
        current_event = models.Event.objects.filter(calendar_id=obj.calendar_id).first()
        if change:
            # Remove all associated old event_receivers.
            EventReceiver.objects.filter(event_id=current_event.id).delete()

        # for account in current_event.accounts.all():
        for account in form.cleaned_data['accounts']:
            new_event_receiver = EventReceiver.objects.create(
                event=current_event,
                account=account
            )
            new_event_receiver.save()
