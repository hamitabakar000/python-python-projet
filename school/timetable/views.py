# timetable/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home_auth.decorators import admin_only
from .models import Timetable
from subject.models import Subject
from teacher.models import Teacher


@login_required
def timetable_list(request):
    timetables = Timetable.objects.all()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    # Group by class and day
    classes = Timetable.objects.values_list('class_name', flat=True).distinct()
    return render(request, 'timetable/timetable.html', {
        'timetables': timetables,
        'days': days,
        'classes': classes,
    })


@login_required
@admin_only
def add_timetable(request):
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        teacher_id = request.POST.get('teacher')
        Timetable.objects.create(
            class_name=request.POST.get('class_name'),
            day=request.POST.get('day'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            subject=Subject.objects.get(id=subject_id) if subject_id else None,
            teacher=Teacher.objects.get(id=teacher_id) if teacher_id else None,
            room=request.POST.get('room', ''),
        )
        messages.success(request, 'Timetable entry added successfully!')
        return redirect('timetable_list')
    return render(request, 'timetable/add-timetable.html', {'subjects': subjects, 'teachers': teachers})


@login_required
@admin_only
def edit_timetable(request, pk):
    entry = get_object_or_404(Timetable, pk=pk)
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        entry.class_name = request.POST.get('class_name', entry.class_name)
        entry.day = request.POST.get('day', entry.day)
        entry.start_time = request.POST.get('start_time', entry.start_time)
        entry.end_time = request.POST.get('end_time', entry.end_time)
        entry.room = request.POST.get('room', entry.room)
        subject_id = request.POST.get('subject')
        teacher_id = request.POST.get('teacher')
        if subject_id:
            entry.subject = Subject.objects.get(id=subject_id)
        if teacher_id:
            entry.teacher = Teacher.objects.get(id=teacher_id)
        entry.save()
        messages.success(request, 'Timetable entry updated successfully!')
        return redirect('timetable_list')
    return render(request, 'timetable/edit-timetable.html', {'entry': entry, 'subjects': subjects, 'teachers': teachers})


@login_required
@admin_only
def delete_timetable(request, pk):
    entry = get_object_or_404(Timetable, pk=pk)
    entry.delete()
    messages.success(request, 'Timetable entry deleted successfully!')
    return redirect('timetable_list')
