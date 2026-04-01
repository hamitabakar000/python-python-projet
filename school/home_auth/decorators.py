from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_superuser or getattr(request.user, 'is_admin', False)):
            messages.error(request, "Accès refusé. Réservé aux administrateurs.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_or_teacher(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_superuser or getattr(request.user, 'is_admin', False) or getattr(request.user, 'is_teacher', False)):
            messages.error(request, "Accès refusé. Réservé aux administrateurs et enseignants.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
