from import_export import resources, fields
from .models import Sender


class SenderResource(resources.ModelResource):
    class Meta:
        model = Sender
        fields = (
            'email',
            'google_oauth2_client_id',
            'google_oauth2_secrete',
            'recovery_email',
            'phone_number',
            'created_at',
            'last_location'
        )
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('email',)
