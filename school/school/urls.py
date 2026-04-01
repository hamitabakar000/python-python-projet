# school/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('faculty.urls')),
    path('student/', include('student.urls')),
    path('authentication/', include('home_auth.urls')),
    path('teacher/', include('teacher.urls')),
    path('department/', include('department.urls')),
    path('subject/', include('subject.urls')),
    path('holiday/', include('holiday.urls')),
    path('timetable/', include('timetable.urls')),
    path('exam/', include('exam.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
