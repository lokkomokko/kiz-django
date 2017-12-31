from django.contrib import admin
from .models import *

class SicksUndergroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_name')

admin.site.register([Med,Sicks, SicksSingle, AgeRange, Table])

admin.site.register(SicksUndergroup, SicksUndergroupAdmin)


