from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from . import models
from . import resources


@admin.register(models.Sender)
class SenderAdmin(ImportExportModelAdmin):
    resource_class = resources.SenderResource
    
    list_display = (
        'id',
        'email',
        'google_oauth2_client_id',
        'recovery_email',
        'phone_number',
        'created_at',
        'last_location',
        'updated_at',
        'description'
    )

    list_display_links = (
        'id',
        'email',
        'google_oauth2_client_id'
    )

    list_per_page = 50

    search_fields = (
        'email',
        'google_oauth2_client_id',
        'recovery_email',
        'phone_number',
        'created_at',
        'last_location'
    )
