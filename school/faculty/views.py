# faculty/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from student.models import Student
from teacher.models import Teacher
from department.models import Department
from subject.models import Subject


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'authentication/login.html')


@login_required
def dashboard(request):
    if hasattr(request.user, 'is_admin') and request.user.is_admin:
        return redirect('admin_dashboard')
    elif hasattr(request.user, 'is_teacher') and request.user.is_teacher:
        return redirect('teacher_dashboard')
    else:
        context = {
            'total_students': Student.objects.count(),
            'total_teachers': Teacher.objects.count(),
            'total_departments': Department.objects.count(),
            'total_subjects': Subject.objects.count(),
        }
        return render(request, 'students/student-dashboard.html', context)


@login_required
def admin_dashboard(request):
    if not (request.user.is_superuser or getattr(request.user, 'is_admin', False)):
        messages.error(request, "Accès refusé. Vous n'êtes pas administrateur.")
        return redirect('dashboard')
    context = {
        'total_students': Student.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'total_departments': Department.objects.count(),
        'total_subjects': Subject.objects.count(),
    }
    return render(request, 'Home/index.html', context)


@login_required
def teacher_dashboard(request):
    if not getattr(request.user, 'is_teacher', False) and not request.user.is_superuser:
        messages.error(request, "Accès refusé. Vous n'êtes pas enseignant.")
        return redirect('dashboard')
    context = {
        'total_students': Student.objects.count(),
        'total_subjects': Subject.objects.count(),
    }
    return render(request, 'Home/teacher-dashboard.html', context)


from django.db.models import Q

@login_required
def search_view(request):
    query = request.GET.get('q', '')
    students = []
    teachers = []
    if query:
        students = Student.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(student_id__icontains=query)
        )
        teachers = Teacher.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(teacher_id__icontains=query)
        )
    context = {
        'query': query,
        'students': students,
        'teachers': teachers
    }
    return render(request, 'Home/search-results.html', context)
