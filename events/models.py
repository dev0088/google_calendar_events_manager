from django.db import models
from senders.models import Sender
from accounts.models import Account
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


class Event(models.Model):
    sender = models.ForeignKey(Sender, related_name='sender_events', on_delete=models.CASCADE)
    summary = models.CharField(max_length=254, blank=True, default='')
    description = models.TextField(blank=True, default='')
    start = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)
    accounts = models.ManyToManyField(
        Account,
        verbose_name=_('accounts'),
        blank=True,
        help_text=_(
            'The accounts this event belongs to. A event will be sent to all accounts '
            'granted to each of their accounts.'
        ),
        related_name='event_set',
        related_query_name='account',
    )
    calendar_id = models.CharField(max_length=1024, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{sender}: {start} - {end}: {summary}".format(
            sender=self.sender.email,
            start=self.start,
            end=self.end,
            summary=self.summary
        )

    class Meta:
        db_table = "events"
        ordering = ('start', 'end', 'sender')
        unique_together = ('id',)
        managed = True


"""
Reminder model for event
"""
class Reminder(models.Model):
    # event = models.ForeignKey(Event, related_name='reminder_events', on_delete=models.CASCADE)
    use_default = models.BooleanField(blank=False, default=False)
    event = models.OneToOneField(
        Event,
        verbose_name=_('event_reminder'),
        related_name='event_reminder',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{overrides}".format(
            overrides=self.reminder_overrides 
        )

    class Meta:
        ordering = ('created_at',)
        unique_together = ('event',)
        verbose_name = _("Reminder")
        verbose_name_plural = _("Reminders")
        managed = True


REMINDER_OVERRIDE_METHODS = (
    ('email', 'email'),
    ('popup', 'popup'),
    ('sms', 'sms'),
)
class Override(models.Model):
    reminder = models.ForeignKey(Reminder, related_name='reminder_overrides', on_delete=models.CASCADE)
    method = models.CharField(max_length=5, blank=False, choices=REMINDER_OVERRIDE_METHODS)
    minutes = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(40320)])

    def __str__(self):
        return "{method}: {minutes} minutes".format(
            method=self.method,
            minutes=self.minutes
        )   
    class Meta:
        verbose_name = _("Override")
        verbose_name_plural = _("Overrides")
