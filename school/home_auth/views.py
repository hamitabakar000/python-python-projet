# home_auth/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, PasswordResetRequest


def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        role = request.POST.get('role', 'student')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'authentication/register.html')

        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        if role == 'student':
            user.is_student = True
        elif role == 'teacher':
            user.is_teacher = True
        elif role == 'admin':
            user.is_admin = True

        user.save()
        login(request, user)
        messages.success(request, 'Signup successful!')
        return redirect('index')

    return render(request, 'authentication/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        user_obj = CustomUser.objects.filter(email=email).first()
        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)
        else:
            user = None
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            if user.is_superuser or (hasattr(user, 'is_admin') and user.is_admin):
                return redirect('admin_dashboard')
            elif hasattr(user, 'is_teacher') and user.is_teacher:
                return redirect('teacher_dashboard')
            elif hasattr(user, 'is_student') and user.is_student:
                return redirect('dashboard')
            else:
                return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'authentication/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        try:
            user = CustomUser.objects.get(email=email)
            reset_request = PasswordResetRequest(user=user, email=email)
            reset_request.save()
            reset_request.send_reset_email()
            messages.success(request, 'Password reset email sent.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'No account found with that email.')
    return render(request, 'authentication/forgot-password.html')


def reset_password_view(request, token):
    try:
        reset_request = PasswordResetRequest.objects.get(token=token)
        if not reset_request.is_valid():
            messages.error(request, 'Reset link has expired.')
            return redirect('forgot_password')

        if request.method == 'POST':
            new_password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')
            if new_password == confirm_password:
                user = reset_request.user
                user.set_password(new_password)
                user.save()
                reset_request.delete()
                messages.success(request, 'Password reset successful.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')

        return render(request, 'authentication/reset_password.html', {'token': token})
    except PasswordResetRequest.DoesNotExist:
        messages.error(request, 'Invalid reset link.')
        return redirect('forgot_password')
