from import_export import resources, fields
from .models import Account


class AccountResource(resources.ModelResource):
    class Meta:
        model = Account
        fields = ('email',)
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('email',)
