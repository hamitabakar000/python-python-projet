# timetable/admin.py
from django.contrib import admin
from .models import Timetable


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'day', 'start_time', 'end_time', 'subject', 'teacher', 'room')
    search_fields = ('class_name', 'room')
    list_filter = ('day', 'class_name', 'teacher')
