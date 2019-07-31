from django.contrib import admin
from . import models


@admin.register(models.Sender)
class SenderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'recovery_email',
        'phone_number',
        'created_at',
        'last_location',
        'updated_at',
        'description'
    )

    list_display_links = (
        'id',
        'email'
    )

    list_per_page = 50
