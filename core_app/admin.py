# admin.py

from django.contrib import admin
from django.contrib.admin.models import LogEntry

admin.site.site_header = 'City Disaster Response'
admin.site.site_title = 'City Disaster Response'
admin.site.index_title = 'City Disaster Response'


class CustomLogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('action_time', 'user', 'content_type')
    search_fields = ('object_repr', 'change_message')
admin.site.register(LogEntry, CustomLogEntryAdmin)
