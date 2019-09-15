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

@admin.register(models.Oauth2Token)
class Oauth2TokenAdmin(admin.ModelAdmin):
    list_display = (
        'sender_display',
        'access_token',
        'refresh_token',
        'token_expiry',
        'code',
        'created_at',
        'updated_at'
    )
    list_display_links = (
        'sender_display',
        'access_token',
        'refresh_token',
        'token_expiry',
        'code',
        'created_at',
        'updated_at'
    )
    list_per_page = 50
    fields = ['sender', 'access_token', 'refresh_token', 'token_expiry', 'code', 'text']

    def sender_display(self, obj):
        return obj.sender.email
