import os
import logging
import json
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from .resources import SenderResource
from .resources import SenderResource
from tablib import Dataset
from oauth2client import client
from senders.forms import RegisterSenderForm
from senders.models import Sender, Oauth2Token
from config import settings


def generate_secret_file_name(sender_id):
    return 'client_secret_{sender_id}.json'.format(sender_id=sender_id)

def make_secret_file(sender_id, client_id, client_secret, client_email):
    secret_data = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token",
            "client_email": client_email,
            "redirect_uris": [
                settings.GOOGLE_CALENDAR_API_REDIRECT_URI
            ],
            "client_x509_cert_url": "",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs"
        }
    }
    file_name = generate_secret_file_name(sender_id)
    # If exist file, remove it.
    if os.path.exists(file_name):
        os.remove(file_name)
    # Create a new file.
    f = open(file_name, "a+")
    f.write(json.dumps(secret_data))
    f.close()
    return file_name

def delete_secret_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


class RegisterSenderView(FormView):

    def authorize_with_google(self, sender_email, client_secret_file_name):
        state = json.dumps({
            'sender_email': sender_email,
        })

        flow = client.flow_from_clientsecrets(
                    client_secret_file_name,
                    settings.GOOGLE_CALENDAR_API_SCOPES,
                    redirect_uri=settings.GOOGLE_CALENDAR_API_REDIRECT_URI
                )
        ###################################################
        # Remote server  mode
        authorize_url = flow.step1_get_authorize_url(redirect_uri=settings.GOOGLE_CALENDAR_API_REDIRECT_URI, state=state)
        logging.info('Go to the following link in your browser: ' + authorize_url)
        return authorize_url

        ##################################################
        # Local host mode
        # storage = Storage('calendar.dat')
        # # credentials = storage.get()
        # flags = google_oauth2_tools.argparser.parse_args([])
        # # flags.noauth_local_webserver = True
        # flags.auth_host_name = 'localhost'
        # flags.auth_host_port = [8000]
        # credentials = google_oauth2_tools.run_flow(self.flow, storage, flags)
        # return credentials
        #######################################################

    def get(self, request, *args, **kwargs):        
        form = RegisterSenderForm()
        context = {'form': form}
        return render(request, 'registration/register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegisterSenderForm(data=request.POST)
        if form.is_valid():
            valid_data = form.cleaned_data
            # Check sender and add it.
            sender = Sender.objects.filter(email=valid_data['email']).first()
            if sender is None:
                sender = Sender.objects.create(
                    email=valid_data['email'],
                    google_oauth2_client_id=valid_data['google_oauth2_client_id'],
                    google_oauth2_secrete=valid_data['google_oauth2_secrete'],
                    recovery_email=valid_data['recovery_email'],
                    phone_number=valid_data['phone_number'],
                    last_location=valid_data['last_location'],
                    description=valid_data['description'],
                )
                sender.save()
            else:
                sender.google_oauth2_client_id=valid_data['google_oauth2_client_id']
                sender.google_oauth2_secrete=valid_data['google_oauth2_secrete']
                sender.recovery_email=valid_data['recovery_email']
                sender.phone_number=valid_data['phone_number']
                sender.last_location=valid_data['last_location']
                sender.description=valid_data['description']
                sender.save()
            
            ######################################################
            # Remote host mode
            client_secret_file_name = make_secret_file(
                sender.id, 
                valid_data['google_oauth2_client_id'], 
                valid_data['google_oauth2_secrete'],
                valid_data['email']
            )
            authorize_url = self.authorize_with_google(valid_data['email'], client_secret_file_name)
            return redirect(authorize_url)
            ######################################################
            # Local host mode
            # credentials = self.authorize_with_google(valid_data)
            # return self.save_credentials(request, sender.id, credentials)
        return redirect(request, 'registration/register.html', {'form': form})

    def save_credentials(self, request, sender_id, credentials):
        logging.info('Sender: {sender}, Credentials: {credentials}'.format(
                sender=sender_id,
                credentials=credentials.to_json()
            )
        )
        if credentials is None or credentials.invalid == True:
            return redirect(
                '/sender/register/failed/?error_message=Failed to create credentials. Please try later.'
            )
        # Save credentials including access token.
        oauth2token = Oauth2Token.objects.filter(sender_id=sender_id).first()
        if oauth2token:
            oauth2token.delete()
        
        str_credentials = credentials.to_json()
        json_credentials = json.loads(str_credentials)
        oauth2token = Oauth2Token.objects.create(
                          sender_id=sender_id,
                          access_token=json_credentials['access_token'],
                          refresh_token=json_credentials['refresh_token'],
                          token_expiry=json_credentials['token_expiry'],
                          text=json.dumps(str_credentials)
                      )
        oauth2token.save

        return redirect(
                    '/sender/register/success/?message=Success to create your account and saved credentials. You can send your events now.'
                )


class SenderAccessToken(FormView):

    def get(self, request, *args, **kwargs):
        # Check parameters
        query_params = request.GET
        query_params = request.GET
        if (not query_params) or (not 'code' in query_params) or (not 'state' in query_params):
            logging.error('Invalid params.')
            error_message = 'Failed step2 wiht invalid parameters.'
            return redirect('/sender/register/failed/?error_message=' + error_message)
        
        code = query_params['code']
        state = json.loads(query_params['state'])
        sender_email = state['sender_email']

        logging.info('Sender: {sender}, Auth code: {code}'.format(
                sender=sender_email,
                code=code
            )
        )

        # Check sender
        sender = Sender.objects.filter(email=sender_email).first()
        if sender is None: 
            logging.error('Failed step2 on google oauth2.')
            error_message = 'Failed step2. Your account wasn\'t created on step1.'
            return redirect('/sender/register/failed/?error_message=' + error_message)

        # Complete step2.
        client_secret_file_name = generate_secret_file_name(sender.id)
        flow = client.flow_from_clientsecrets(
                    client_secret_file_name,
                    settings.GOOGLE_CALENDAR_API_SCOPES,
                    redirect_uri=settings.GOOGLE_CALENDAR_API_REDIRECT_URI
                )
        credentials = flow.step2_exchange(code)
        delete_secret_file(client_secret_file_name)
        logging.info('Sender: {sender}, Credentials: {credentials}'.format(
                sender=sender.email,
                credentials=credentials.to_json()
            )
        )
        logging.info('credentials: {}'.format(credentials.to_json()))
        str_credentials = credentials.to_json()
        json_credentials = json.loads(str_credentials)
        # Save credentials including access token.
        oauth2token = Oauth2Token.objects.filter(sender_id=sender.id).first()
        if oauth2token:
            oauth2token.delete()
        
        # Save credentials including access token.
        oauth2token = Oauth2Token.objects.filter(sender_id=sender.id).first()
        if oauth2token:
            oauth2token.delete()
        
        oauth2token = Oauth2Token.objects.create(
                          sender_id=sender.id,
                          access_token=json_credentials['access_token'],
                          refresh_token=json_credentials['refresh_token'],
                          token_expiry=json_credentials['token_expiry'],
                          code=code,
                          text=json.dumps(json_credentials)
                      )
        oauth2token.save

        message = 'Success to create your account and saved credentials. You can send your events now.'
        return redirect('/sender/register/success/?message=' + message)


class RegisterSenderSuccessView(FormView):
    def get(self, request, *args, **kwargs):
        return render(
                    request, 
                    'registration/success.html', 
                    {'message': request.GET['message']}
                )


class RegisterSenderFailedView(FormView):
    def get(self, request, *args, **kwargs):
        return render(
                    request, 
                    'registration/failed.html', 
                    {'error_message': request.GET['error_message']}
                )


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
        result = sender_resource.import_data(dataset, dry_run=True)

        if not result.has_errors():
            sender_resource.import_data(dataset, dry_run=False)

    return render(request, 'core/simple_upload.html')
