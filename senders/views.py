from django.shortcuts import render
from django.http import HttpResponse
from .resources import SenderResource
from tablib import Dataset


def export_csv(request):
    sender_resource = SenderResource()
    dataset = sender_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="senders.csv"'
    return response

def export_json(request):
    sender_resource = SenderResource()
    dataset = sender_resource.export()
    response = HttpResponse(dataset.json, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="senders.json"'
    return response

def export_excel(request):
    sender_resource = SenderResource()
    dataset = sender_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="senders.xls"'
    return response

def simple_upload(request):
    if request.method == 'POST':
        sender_resource = SenderResource()
        dataset = Dataset()
        new_senders = request.FILES['csvfile']

        imported_data = dataset.load(new_senders.read())
        result = sender_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            sender_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'core/simple_upload.html')