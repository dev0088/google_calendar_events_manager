from django.db import models


class Sender(models.Model):
    email = models.CharField(max_length=254, blank=False)
    google_oauth2_client_id = models.CharField(max_length=254, blank=True, default='')
    google_oauth2_secrete = models.CharField(max_length=254, blank=True, default='')
    recovery_email = models.CharField(max_length=254, blank=True, default='')
    phone_number = models.CharField(max_length=20, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    last_location = models.CharField(max_length=150, blank=True, default='')
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return "{email}".format(email=self.email)

    class Meta:
        db_table = "senders"
        ordering = ('email',)
        unique_together = ('email',)
        managed = True
