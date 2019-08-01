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
def google_calendar_connection():
    """
    This method used for connect with google calendar api.
    """
    
    flags = tools.argparser.parse_args([])
    
    redirect_uri = settings.GOOGLE_CALENDAR_API_REDIRECT_URI
    if not redirect_uri:
        httpd = tools.ClientRedirectServer(('localhost', 0), tools.ClientRedirectHandler)
        httpd.timeout = 60
        redirect_uri = 'http://%s:%s/' % httpd.server_address        
    print( redirect_uri )

    flow = OAuth2WebServerFlow(
        client_id=settings.GOOGLE_CALENDAR_API_CLIENT_ID, 
        client_secret=settings.GOOGLE_CALENDAR_API_CLIENT_SECRET,
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

def add_event():
    service = google_calendar_connection()
    
    event = {
        'summary': 'Google I/O 2015',
        'location': '800 Howard St., San Francisco, CA 94103',
        'description': "anything",
        'start': {
            'dateTime': '2019-08-03T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2019-08-03T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
    }
    
    event = service.events().insert(calendarId='primary', body=event).execute()