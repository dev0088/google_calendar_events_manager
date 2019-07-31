from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from . import models
from . import resources


@admin.register(models.Account)
class AccountAdmin(ImportExportModelAdmin):
    resource_class = resources.AccountResource

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

    search_fields = (
        'email',
    )
