from django.contrib import admin
from . import models
from . import google_calendar

@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'creator',
        'summary',
        'start',
        'end',
        'created_at',
        'updated_at'
    )

    list_display_links = (
        'id',
        'creator',
        'summary',
        'start',
        'end',
    )
    
    list_per_page = 50

    def creator(self, obj):
        return obj.creator.email

    def save_model(self, request, obj, form, change):
        print(obj)
        service = google_calendar.google_calendar_connection()
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
            # 'recurrence': [
            #     'RRULE:FREQ=DAILY;COUNT=2'
            # ],
            'attendees': [
                {'email': 'valeriiadidushok@gmail.com'},
                {'email': 'marcrochon888@gmail.com'},
                {'email': 'sydorov.upwk@gmail.com'},
            ],
            # 'reminders': {
            #     'useDefault': False,
            #     'overrides': [
            #     {'method': 'email', 'minutes': 24 * 60},
            #     {'method': 'popup', 'minutes': 10},
            #     ],
            # },
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('======================')
        print(event)
        print ('Event created: %s' % (event.get('htmlLink')))
        print('======================')
        super().save_model(request, obj, form, change)