from django.shortcuts import render
from googleapiclient import discovery, sample_tools
from googleapiclient.errors import HttpError
from googleapiclient.http import BatchHttpRequest
from oauth2client import client, tools
from oauth2client.client import OAuth2WebServerFlow, AccessTokenCredentials
from oauth2client.file import Storage
from google_auth_oauthlib.flow import InstalledAppFlow
from config import settings
import httplib2shim
import google.auth
import requests
import json
import ssl
import logging

SCOPES = 'https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/calendar.events'
#---------------------------------------------------------------------------
# google_calendar_connection
#---------------------------------------------------------------------------
def google_calendar_raw_connection(oauth2_clinet_id, oauth2_secrete, sender_id, change, org_credentials):
    """
    This method used for connect with google calendar api.
    """
    if not org_credentials:
        error_message = 'This sender {sender_id} don\'t have oauth2 access-token, yet. Please send this link {register_link} to the sender. So he can register with his google account, again.'.format(
            sender_id=sender_id,
            register_link=settings.REGISTER_URL
        )
        logging.error(error_message)
        return None
    else:
        json_credentials = json.loads(org_credentials)
        credentials = client.GoogleCredentials(None,
            json_credentials['client_id'],
            json_credentials['client_secret'],
            json_credentials['refresh_token'],
            json_credentials['token_expiry'],
            "https://accounts.google.com/o/oauth2/token",
            None
        )
        
    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with our good Credentials.
    http = httplib2shim.Http()
    http = credentials.authorize(http)
    service = discovery.build('calendar', 'v3', http=http)

    return {
        'http': http,
        'service': service
    }

def google_calendar_connection(oauth2_clinet_id, oauth2_secrete, sender_id, change, org_credentials=None):
    """
    This method used for connect with google calendar api.
    """
    raw_connection = google_calendar_raw_connection(
        oauth2_clinet_id, 
        oauth2_secrete, 
        sender_id,
        change,
        org_credentials
    )
    if raw_connection:
        return raw_connection['service']
    
    return None

def add_event(event, oauth2_clinet_id, oauth2_secrete):
    service = google_calendar_connection(oauth2_clinet_id, oauth2_secrete)
    try:
        event = service.events().insert(
            calendarId=settings.GOOGLE_CALENDAR_API_DEFAULT_CALENDAR_ID, 
            body=event
        ).execute()
        print('====== add_event: ', event)
    except HttpError as e:
        print('====== add_event: error: ', e)
        if e.resp.status==404:
            return None
    return event

def update_event(event_id, event, oauth2_clinet_id, oauth2_secrete):
    service = google_calendar_connection(oauth2_clinet_id, oauth2_secrete)
    try:
        origin_event = service.events().get(
            calendarId=settings.GOOGLE_CALENDAR_API_DEFAULT_CALENDAR_ID, 
            eventId=event_id
        ).execute()
        print('====== get_event: ', origin_event)
        updated_event = service.events().update(
            calendarId=settings.GOOGLE_CALENDAR_API_DEFAULT_CALENDAR_ID, 
            eventId=event_id, 
            body=event
        ).execute()
        print('====== updated_event: ', updated_event)
    except HttpError as e:
        print('====== update_event: error: ', e)
        if e.resp.status==404:
            return None
    return updated_event

def delete_event(event_id, oauth2_clinet_id, oauth2_secrete):
    service = google_calendar_connection(oauth2_clinet_id, oauth2_secrete)
    try:
        res = service.events().delete(
            calendarId=settings.GOOGLE_CALENDAR_API_DEFAULT_CALENDAR_ID, 
            eventId=event_id
        ).execute()
        print('====== delete_event: ', res)
    except HttpError as e:
        print('====== delete_event: error: ', e)
        return False
    return True

def batch_add_events(events, oauth2_clinet_id, oauth2_secrete, sender_id, change, org_credentials, callback):
    raw_connection = google_calendar_raw_connection(
        oauth2_clinet_id, 
        oauth2_secrete,
        sender_id,
        change,
        org_credentials
    )
    http = raw_connection['http']
    service = raw_connection['service']
    batch = BatchHttpRequest()

    for event in events:
        batch.add(service.events().insert(
                calendarId=settings.GOOGLE_CALENDAR_API_DEFAULT_CALENDAR_ID, 
                body=event
            ),
            callback
        )
    
    batch.execute(http=http)

def batch_update_events(event_ids, events, oauth2_clinet_id, oauth2_secrete, sender_id, change, org_credentials, callback):
    raw_connection = google_calendar_raw_connection(
        oauth2_clinet_id, 
        oauth2_secrete,
        sender_id,
        change,
        org_credentials
    )
    http = raw_connection['http']
    service = raw_connection['service']
    batch = BatchHttpRequest()

    index = 0
    for event_id in event_ids:
        batch.add(service.events().update(
                calendarId=settings.GOOGLE_CALENDAR_API_DEFAULT_CALENDAR_ID, 
                eventId=event_id, 
                body=events[index]
            ),
            callback
        )
        index = index + 1
    
    batch.execute(http=http)

def batch_delete_events(event_ids, oauth2_clinet_id, oauth2_secrete, sender_id, change, org_credentials, callback):
    raw_connection = google_calendar_raw_connection(
        oauth2_clinet_id, 
        oauth2_secrete,
        sender_id,
        change,
        org_credentials
    )
    http = raw_connection['http']
    service = raw_connection['service']
    batch = BatchHttpRequest()

    index = 0
    for event_id in event_ids:
        batch.add(
            service.events().delete(
                calendarId=settings.GOOGLE_CALENDAR_API_DEFAULT_CALENDAR_ID, 
                eventId=event_id
            ),
            callback
        )
        index = index + 1
    
    batch.execute(http=http)