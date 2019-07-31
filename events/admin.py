from django.contrib import admin
from . import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'creator',
        'summary',
        'start',
        'end',
        'created_at',
        'updated_at'
    )

    list_display_links = (
        'id',
        'creator',
        'summary',
        'start',
        'end',
    )
    
    list_per_page = 50

    def creator(self, obj):
        return obj.creator.email