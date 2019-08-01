from django.shortcuts import render
from googleapiclient import discovery
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import httplib2
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
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = discovery.build('calendar', 'v3', http=http)
    
    return service

def add_event(event, oauth2_clinet_id, oauth2_secrete):
    service = google_calendar_connection(oauth2_clinet_id, oauth2_secrete)
    return service.events().insert(calendarId='primary', body=event).execute()
