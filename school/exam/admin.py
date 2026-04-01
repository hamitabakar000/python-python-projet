# exam/admin.py
from django.contrib import admin
from .models import Exam, ExamResult


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'class_name', 'exam_date', 'start_time', 'end_time', 'total_marks')
    search_fields = ('name', 'class_name')
    list_filter = ('exam_date', 'class_name', 'subject')


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'marks_obtained', 'grade')
    search_fields = ('student__first_name', 'student__last_name', 'exam__name')
    list_filter = ('grade', 'exam')
