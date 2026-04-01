# exam/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home_auth.decorators import admin_or_teacher
from .models import Exam, ExamResult
from subject.models import Subject
from student.models import Student


@login_required
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'exams/exams.html', {'exams': exams})


@login_required
@admin_or_teacher
def add_exam(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        Exam.objects.create(
            name=request.POST.get('name'),
            exam_date=request.POST.get('exam_date'),
            subject=Subject.objects.get(id=subject_id) if subject_id else None,
            class_name=request.POST.get('class_name'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            total_marks=request.POST.get('total_marks', 100),
        )
        messages.success(request, 'Exam added successfully!')
        return redirect('exam_list')
    return render(request, 'exams/add-exam.html', {'subjects': subjects})


@login_required
@admin_or_teacher
def edit_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    subjects = Subject.objects.all()
    if request.method == 'POST':
        exam.name = request.POST.get('name', exam.name)
        exam.exam_date = request.POST.get('exam_date', exam.exam_date)
        exam.class_name = request.POST.get('class_name', exam.class_name)
        exam.start_time = request.POST.get('start_time', exam.start_time)
        exam.end_time = request.POST.get('end_time', exam.end_time)
        exam.total_marks = request.POST.get('total_marks', exam.total_marks)
        subject_id = request.POST.get('subject')
        if subject_id:
            exam.subject = Subject.objects.get(id=subject_id)
        exam.save()
        messages.success(request, 'Exam updated successfully!')
        return redirect('exam_list')
    return render(request, 'exams/edit-exam.html', {'exam': exam, 'subjects': subjects})


@login_required
@admin_or_teacher
def delete_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    exam.delete()
    messages.success(request, 'Exam deleted successfully!')
    return redirect('exam_list')


@login_required
def exam_results(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    results = ExamResult.objects.filter(exam=exam)
    return render(request, 'exams/exam-results.html', {'exam': exam, 'results': results})


@login_required
@admin_or_teacher
def add_result(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    students = Student.objects.all()
    if request.method == 'POST':
        student_id = request.POST.get('student')
        ExamResult.objects.create(
            exam=exam,
            student=Student.objects.get(id=student_id),
            marks_obtained=request.POST.get('marks_obtained'),
            remarks=request.POST.get('remarks', ''),
        )
        messages.success(request, 'Result added successfully!')
        return redirect('exam_results', exam_id=exam.id)
    return render(request, 'exams/add-result.html', {'exam': exam, 'students': students})


@login_required
@admin_or_teacher
def edit_result(request, pk):
    result = get_object_or_404(ExamResult, pk=pk)
    if request.method == 'POST':
        result.marks_obtained = request.POST.get('marks_obtained', result.marks_obtained)
        result.remarks = request.POST.get('remarks', result.remarks)
        result.save()
        messages.success(request, 'Result updated successfully!')
        return redirect('exam_results', exam_id=result.exam.id)
    return render(request, 'exams/edit-result.html', {'result': result})


@login_required
@admin_or_teacher
def delete_result(request, pk):
    result = get_object_or_404(ExamResult, pk=pk)
    exam_id = result.exam.id
    result.delete()
    messages.success(request, 'Result deleted successfully!')
    return redirect('exam_results', exam_id=exam_id)
