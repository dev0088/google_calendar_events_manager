from django.db import models

class Account(models.Model):
    email = models.CharField(max_length=254, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return "{email}".format(email=self.email)

    class Meta:
        db_table = "accounts"
        ordering = ('id',)
        unique_together = ('email', 'id')
        managed = True
