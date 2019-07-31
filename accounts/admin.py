from django.contrib import admin
from . import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'created_at',
        'updated_at',
        'description'
    )

    list_display_links = (
        'id',
        'email'
    )

    list_per_page = 50
