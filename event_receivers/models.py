from django.db import models
from events.models import Event
from accounts.models import Account


class EventReceiver(models.Model):
    event = models.ForeignKey(Event, related_name='event_receivers', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, related_name='account_receivers', on_delete=models.CASCADE)
    opened = models.BooleanField(default=False)
    clicked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{sender}->{receiver}: {event}".format(
            sender=self.event.creator.email,
            receiver=self.account.email,
            event=self.event.summary
        )

    class Meta:
        db_table = "event_receivers"
        ordering = ('id',)
        unique_together = ('event', 'account')
        managed = True
