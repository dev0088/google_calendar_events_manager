from django.shortcuts import render
from googleapiclient import discovery
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import httplib2
import httplib2shim
import ssl
# from events import socks
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
    # ssl._create_default_https_context = ssl._create_unverified_context
    # print(
    #     settings.SMART_PROXY_ADDRESS, 
    #     settings.SMART_PROXY_PORT, 
    #     settings.SMART_PROXY_USER_NAME, 
    #     settings.SMART_PROXY_PASSWORD
    # )
    # proxy_info = httplib2.ProxyInfo(
    #     httplib2.socks.PROXY_TYPE_HTTP, 
    #     settings.SMART_PROXY_ADDRESS, 
    #     settings.SMART_PROXY_PORT, 
    #     proxy_user = settings.SMART_PROXY_USER_NAME, 
    #     proxy_pass = settings.SMART_PROXY_PASSWORD
    # )
    # http = httplib2.Http(proxy_info = proxy_info)
    http = credentials.authorize(http)
    service = discovery.build('calendar', 'v3', http=http)
    
    return service

def add_event(event, oauth2_clinet_id, oauth2_secrete):
    service = google_calendar_connection(oauth2_clinet_id, oauth2_secrete)
    return service.events().insert(calendarId='primary', body=event).execute()
