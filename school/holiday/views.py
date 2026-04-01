# holiday/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home_auth.decorators import admin_only
from .models import Holiday


@login_required
def holiday_list(request):
    holidays = Holiday.objects.all()
    return render(request, 'holidays/holidays.html', {'holidays': holidays})


@login_required
@admin_only
def add_holiday(request):
    if request.method == 'POST':
        Holiday.objects.create(
            name=request.POST.get('name'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            description=request.POST.get('description', ''),
            holiday_type=request.POST.get('holiday_type', 'Public'),
        )
        messages.success(request, 'Holiday added successfully!')
        return redirect('holiday_list')
    return render(request, 'holidays/add-holiday.html')


@login_required
@admin_only
def edit_holiday(request, pk):
    holiday = get_object_or_404(Holiday, pk=pk)
    if request.method == 'POST':
        holiday.name = request.POST.get('name', holiday.name)
        holiday.start_date = request.POST.get('start_date', holiday.start_date)
        holiday.end_date = request.POST.get('end_date', holiday.end_date)
        holiday.description = request.POST.get('description', holiday.description)
        holiday.holiday_type = request.POST.get('holiday_type', holiday.holiday_type)
        holiday.save()
        messages.success(request, 'Holiday updated successfully!')
        return redirect('holiday_list')
    return render(request, 'holidays/edit-holiday.html', {'holiday': holiday})


@login_required
@admin_only
def delete_holiday(request, pk):
    holiday = get_object_or_404(Holiday, pk=pk)
    holiday.delete()
    messages.success(request, 'Holiday deleted successfully!')
    return redirect('holiday_list')
