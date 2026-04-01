# subject/admin.py
from django.contrib import admin
from .models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'teacher')
    search_fields = ('name', 'code')
    list_filter = ('department',)
