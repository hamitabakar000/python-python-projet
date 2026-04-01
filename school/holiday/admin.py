# holiday/admin.py
from django.contrib import admin
from .models import Holiday


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'holiday_type')
    search_fields = ('name',)
    list_filter = ('holiday_type', 'start_date')
