from django.shortcuts import render
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import httplib2shim
import ssl
from config import settings

#---------------------------------------------------------------------------
# google_calendar_connection
#---------------------------------------------------------------------------
def google_calendar_connection(oauth2_clinet_id, oauth2_secrete):
    """
    This method used for connect with google calendar api.
    """
    
    flags = tools.argparser.parse_args([])
    
    redirect_uri = settings.GOOGLE_CALENDAR_API_REDIRECT_URI
    if not redirect_uri:
        httpd = tools.ClientRedirectServer(('localhost', 0), tools.ClientRedirectHandler)
        httpd.timeout = 60
        redirect_uri = 'http://%s:%s/' % httpd.server_address        

    flow = OAuth2WebServerFlow(
        client_id=oauth2_clinet_id, 
        client_secret=oauth2_secrete,
        redirect_uri=redirect_uri,
        scope='https://www.googleapis.com/auth/calendar',
        user_agent=settings.GOOGLE_CALENDAR_API_APP_NAME
        )
    storage = Storage('calendar.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid == True:
        credentials = tools.run_flow(flow, storage, flags)
    
    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with our good Credentials.
    http = httplib2shim.Http()
    http = credentials.authorize(http)
    service = discovery.build('calendar', 'v3', http=http)
    
    return service


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
            eventId='eventId'
        ).execute()
        print('====== delete_event: ', res)
    except HttpError as e:
        print('====== delete_event: error: ', e)
        return False
    return True
    