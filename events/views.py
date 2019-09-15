from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from events.models import Event
from senders.models import Sender, Oauth2Token
import json

class EventAccessToken(APIView):

    def get(self, request, format=None):
        user = request.user

        print ('==== get: ', request.query_params)
        # Check parameters
        query_params = request.query_params
        if (not query_params) or (query_params['code'] is None) or (query_params['state'] is None):
            print('===== invalid params.')
            return Response()

        code = query_params['code']
        state = json.loads(query_params['state'])
        sender_email = state['sender_email']

        print ('==== get: code: ', code)
        print('===== get: state[0]: ', query_params['state'])
        print ('==== get: state: ', state)       
        print ('==== sender_email: ', sender_email)

        sender = Sender.objects.filter(email=sender_email).first()
        if sender: 
            sender_id = sender.id
        else:
            return Response()
            
        oauth2token = Oauth2Token.objects.filter(sender_id=sender_id).first()
        if oauth2token:
            oauth2token.delete()
        
        oauth2token = Oauth2Token.objects.create(
                        sender_id=sender_id,
                        code=code
                      )
        oauth2token.save

        return Response()

    def post(self, request, format=None):
        self.update_oauth2tocken(request, format)
        return Response()

    def put(self, request, format=None):
        self.update_oauth2tocken(request, format)
        return Response()
    
    def update_oauth2tocken(self, request, format=None):
        user = request.user
        print('===== post:', request.query_params)
        sender_id = request.query_params['sender_id']
        credentials = json.loads(request.query_params['credentials'])
        print('===== credentials: ', credentials)
        oauth2token = Oauth2Token.objects.filter(sender_id=sender_id).first()
        code = ''
        if oauth2token:
            code = oauth2token.code
            oauth2token.delete()

        oauth2token = Oauth2Token.objects.create(
                          sender_id=sender_id,
                          access_token=credentials['access_token'],
                          refresh_token=credentials['refresh_token'],
                          token_expiry=credentials['token_expiry'],
                          code=code,
                          text=request.query_params['credentials']
                      )
        oauth2token.save