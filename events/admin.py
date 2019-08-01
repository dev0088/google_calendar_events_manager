from django.contrib import admin
from django.contrib.admin import widgets
# from events.multiselect import widget
from . import models
from . import google_calendar



@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sender_display',
        'summary',
        'start',
        'end',
        'accounts_display',
        'created_at',
        'updated_at'
    )

    list_display_links = (
        'id',
        'sender_display',
        'summary',
        'start',
        'end',
    )
    
    list_per_page = 50  
    filter_horizontal = ('accounts',)
    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     vertical = False  # change to True if you prefer boxes to be stacked vertically
    #     kwargs['widget'] = widgets.FilteredSelectMultiple(
    #         db_field.verbose_name,
    #         vertical,
    #     )
    #     return super(EventAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


    def sender_display(self, obj):
        return obj.sender.email

    def accounts_display(self, obj):
        return ''

    sender_display.short_description = "Sender"
    accounts_display.short_description = "Accounts"


    def save_model(self, request, obj, form, change):
        print(obj)
        service = google_calendar.google_calendar_connection()
        event = {
            'summary': 'For Sydorov',
            # 'location': '800 Howard St., San Francisco, CA 94103',
            'description': "Sydorov, show this",
            'start': {
                'dateTime': '2019-08-04T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2019-08-04T17:00:00-07:00',
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