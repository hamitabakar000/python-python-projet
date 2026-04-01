# teacher/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home_auth.decorators import admin_only
from .models import Teacher
from department.models import Department


@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teachers.html', {'teachers': teachers})


@login_required
@admin_only
def add_teacher(request):
    departments = Department.objects.all()
    if request.method == 'POST':
        dept_id = request.POST.get('department')
        dept = Department.objects.get(id=dept_id) if dept_id else None
        Teacher.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            teacher_id=request.POST.get('teacher_id'),
            gender=request.POST.get('gender'),
            date_of_birth=request.POST.get('date_of_birth'),
            mobile_number=request.POST.get('mobile_number'),
            email=request.POST.get('email'),
            joining_date=request.POST.get('joining_date'),
            qualification=request.POST.get('qualification'),
            experience=request.POST.get('experience', ''),
            department=dept,
            address=request.POST.get('address', ''),
            teacher_image=request.FILES.get('teacher_image'),
        )
        messages.success(request, 'Teacher added successfully!')
        return redirect('teacher_list')
    return render(request, 'teachers/add-teacher.html', {'departments': departments})


@login_required
@admin_only
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    departments = Department.objects.all()
    if request.method == 'POST':
        teacher.first_name = request.POST.get('first_name', teacher.first_name)
        teacher.last_name = request.POST.get('last_name', teacher.last_name)
        teacher.gender = request.POST.get('gender', teacher.gender)
        teacher.date_of_birth = request.POST.get('date_of_birth', teacher.date_of_birth)
        teacher.mobile_number = request.POST.get('mobile_number', teacher.mobile_number)
        teacher.email = request.POST.get('email', teacher.email)
        teacher.joining_date = request.POST.get('joining_date', teacher.joining_date)
        teacher.qualification = request.POST.get('qualification', teacher.qualification)
        teacher.experience = request.POST.get('experience', teacher.experience)
        teacher.address = request.POST.get('address', teacher.address)
        dept_id = request.POST.get('department')
        if dept_id:
            teacher.department = Department.objects.get(id=dept_id)
        if request.FILES.get('teacher_image'):
            teacher.teacher_image = request.FILES.get('teacher_image')
        teacher.save()
        messages.success(request, 'Teacher updated successfully!')
        return redirect('teacher_list')
    return render(request, 'teachers/edit-teacher.html', {'teacher': teacher, 'departments': departments})


@login_required
def view_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    return render(request, 'teachers/teacher-details.html', {'teacher': teacher})


@login_required
@admin_only
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    teacher.delete()
    messages.success(request, 'Teacher deleted successfully!')
    return redirect('teacher_list')
