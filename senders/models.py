from django.db import models
from django.utils.translation import ugettext_lazy as _


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


class Oauth2Token(models.Model):
    sender = models.OneToOneField(
        Sender,
        related_name='sender_oauth2token',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    access_token = models.CharField(max_length=254, blank=False, default='')
    refresh_token = models.CharField(max_length=254, blank=False, default='')
    token_expiry = models.CharField(max_length=254, blank=False, default='')
    code = models.CharField(max_length=254, blank=True)
    text = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{access_token}'.format(access_token=self.access_token)

    class Meta:
        ordering = ('sender', 'updated_at')
        unique_together = ('sender',)
        verbose_name = _("SenderOauth2Token")
        verbose_name_plural = _("SenderOauth2Tokens")
        managed = True
