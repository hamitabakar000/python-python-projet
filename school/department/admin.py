# department/admin.py
from django.contrib import admin
from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'date_created')
    search_fields = ('name',)
    list_filter = ('date_created',)
