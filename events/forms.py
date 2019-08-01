from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from accounts.models import Account


# class AccountManageForm(forms.Form):
#     accounts = forms.ModelMultipleChoiceField(
#         queryset=Account.objects.all(),
#         required=True,
#         widget=FilteredSelectMultiple("Accounts", is_stacked=False)
#     )

# class Media:
#     css = {'all': ('/static/admin/css/widgets.css',), }
#     js = ('/admin/jsi18n/',)

# def __init__(self, parents=None, *args, **kwargs):
#     super(AccountManageForm, self).__init__(*args, **kwargs)

class AccountManageForm(forms.ModelForm):

    class Meta:
        model = Account
        exclude = ['email']