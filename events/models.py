from django.db import models
from senders.models import Sender
from accounts.models import Account
from django.utils.translation import ugettext_lazy as _

class Event(models.Model):
    sender = models.ForeignKey(Sender, related_name='sender_events', on_delete=models.CASCADE)
    calendar_id = models.CharField(max_length=1024, blank=True, default='')
    summary = models.TextField(blank=True, default='')
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
        related_name="event_set",
        related_query_name="account",
    )
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
