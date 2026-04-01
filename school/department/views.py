# department/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home_auth.decorators import admin_only
from .models import Department
from teacher.models import Teacher


@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/departments.html', {'departments': departments})


@login_required
@admin_only
def add_department(request):
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        head_id = request.POST.get('head')
        head = Teacher.objects.get(id=head_id) if head_id else None
        Department.objects.create(
            name=request.POST.get('name'),
            head=head,
            description=request.POST.get('description', ''),
        )
        messages.success(request, 'Department added successfully!')
        return redirect('department_list')
    return render(request, 'departments/add-department.html', {'teachers': teachers})


@login_required
@admin_only
def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        department.name = request.POST.get('name', department.name)
        department.description = request.POST.get('description', department.description)
        head_id = request.POST.get('head')
        department.head = Teacher.objects.get(id=head_id) if head_id else None
        department.save()
        messages.success(request, 'Department updated successfully!')
        return redirect('department_list')
    return render(request, 'departments/edit-department.html', {'department': department, 'teachers': teachers})


@login_required
@admin_only
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    messages.success(request, 'Department deleted successfully!')
    return redirect('department_list')
