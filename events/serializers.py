from rest_framework import serializers
from .models import Event, Reminder, Override


class OverrideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Override
        fields = ('method', 'minutes',)


class ReminderSerializer(serializers.ModelSerializer):
    overrides = OverrideSerializer(many=True, required=False)
    
    class Meta:
        model = Reminder
        fields = ('useDefault', 'overrides',)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'