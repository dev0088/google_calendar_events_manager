from rest_framework import serializers
from .models import Event, Reminder, Override, Recurrence, CalendarEvent
from accounts.serializers import AccountSerializer


class CalendarEventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CalendarEvent
        fields = (
            'calendar_event_id',
            'event',
        )

class OverrideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Override
        fields = ('method', 'minutes',)


class ReminderSerializer(serializers.ModelSerializer):
    overrides = OverrideSerializer(many=True, required=False)
    
    class Meta:
        model = Reminder
        fields = ('useDefault', 'overrides',)


class RecurrenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurrence
        fields = (
            'event',
            'rule',
            'freq',
            'count',
            'ends',
            'until',
            'interval',
        )


class EventSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True, required=False)
    reminder = ReminderSerializer(many=False, required=False)
    recurrences = RecurrenceSerializer(many=True, required=False)
    calendar_event_events = CalendarEventSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = (
            'sender',
            'summary',
            'description',
            'start',
            'end',
            'accounts',
            'reminder',
            'recurrences',
            'calendar_event_events'
        )
