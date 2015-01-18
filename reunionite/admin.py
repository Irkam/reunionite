'''
Created on 26 déc. 2014

@author: Jean-Vincent
'''

from reunionite.models import *
from django.contrib import admin

class DateLinkInline(admin.TabularInline):
    model = Date
    
class MeetingAdmin(admin.ModelAdmin):
    fieldset = [
                (None, {'fields': ['name', 'description', 'open',]}),
                ('Date', {'fields': ['date_created', 'date_closed',]}),
                ('Restrictions', {'fields': ['restrict_registered', 'restrict_group',]}),
                ]
    inlines = [DateLinkInline]


class AvailabilitiesInline(admin.TabularInline):
    model = Availability

class DateAdmin(admin.ModelAdmin):
    inlines = [AvailabilitiesInline]

admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Date, DateAdmin)
admin.site.register(Availability)