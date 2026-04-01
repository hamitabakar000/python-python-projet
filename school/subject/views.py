# subject/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home_auth.decorators import admin_only
from .models import Subject
from department.models import Department
from teacher.models import Teacher


@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects/subjects.html', {'subjects': subjects})


@login_required
@admin_only
def add_subject(request):
    departments = Department.objects.all()
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        dept_id = request.POST.get('department')
        teacher_id = request.POST.get('teacher')
        Subject.objects.create(
            name=request.POST.get('name'),
            code=request.POST.get('code'),
            department=Department.objects.get(id=dept_id) if dept_id else None,
            teacher=Teacher.objects.get(id=teacher_id) if teacher_id else None,
            description=request.POST.get('description', ''),
        )
        messages.success(request, 'Subject added successfully!')
        return redirect('subject_list')
    return render(request, 'subjects/add-subject.html', {'departments': departments, 'teachers': teachers})


@login_required
@admin_only
def edit_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    departments = Department.objects.all()
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        subject.name = request.POST.get('name', subject.name)
        subject.code = request.POST.get('code', subject.code)
        subject.description = request.POST.get('description', subject.description)
        dept_id = request.POST.get('department')
        teacher_id = request.POST.get('teacher')
        if dept_id:
            subject.department = Department.objects.get(id=dept_id)
        if teacher_id:
            subject.teacher = Teacher.objects.get(id=teacher_id)
        subject.save()
        messages.success(request, 'Subject updated successfully!')
        return redirect('subject_list')
    return render(request, 'subjects/edit-subject.html', {'subject': subject, 'departments': departments, 'teachers': teachers})


@login_required
@admin_only
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    subject.delete()
    messages.success(request, 'Subject deleted successfully!')
    return redirect('subject_list')
