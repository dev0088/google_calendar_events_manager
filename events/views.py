from django.shortcuts import render
from accounts.models import Account


class AccountManageView(DetailView):
    model = Account
    template_name = 'accounts/account_manage.html'

    def get_context_data(self, **kwargs):
    context = super(AccountManageView, self).get_context_data(**kwargs)
    context['form'] = AccountManageForm()
    return context