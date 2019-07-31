from django.shortcuts import render
from django.http import HttpResponse
from .resources import AccountResource
from tablib import Dataset


def export_csv(request):
    account_resource = AccountResource()
    dataset = account_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="accounts.csv"'
    return response

def export_json(request):
    account_resource = AccountResource()
    dataset = account_resource.export()
    response = HttpResponse(dataset.json, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="accounts.json"'
    return response

def export_excel(request):
    account_resource = AccountResource()
    dataset = account_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="accounts.xls"'
    return response

def simple_upload(request):
    if request.method == 'POST':
        account_resource = AccountResource()
        dataset = Dataset()
        new_accounts = request.FILES['csvfile']

        imported_data = dataset.load(new_accounts.read())
        result = account_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            account_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'core/simple_upload.html')