from django.db import models
from senders.models import Sender


class Event(models.Model):
    creator = models.ForeignKey(Sender, related_name='sender_events', on_delete=models.CASCADE)
    calendar_id = models.CharField(max_length=1024, blank=True, default='')
    summary = models.TextField(blank=True, default='')
    start = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{creator}\n{start} - {end}\n{summary}".format(
            creator=self.creator.email,
            start=self.start,
            end=self.end,
            summary=self.summary
        )

    class Meta:
        db_table = "events"
        ordering = ('start', 'end', 'creator')
        unique_together = ('calendar_id',)
        managed = True
