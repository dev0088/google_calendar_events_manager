from import_export import resources, fields
from .models import Sender


class SenderResource(resources.ModelResource):
    class Meta:
        model = Sender
        fields = (
            'email',
            'password',
            'recovery_email',
            'phone_number',
            'created_at',
            'last_location'
        )
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('email',)
        # import_id_fields = [
        #     'email', 
        #     'password', 
        #     'recovery_email',
        #     'phone_number',
        # ]
        # exclude = [
        #     'id',
        #     'email', 
        #     'password', 
        #     'recovery_email',
        #     'phone_number',
        #     'created_at',
        #     'last_location'
        # ]
