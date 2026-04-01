# exam/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('add/', views.add_exam, name='add_exam'),
    path('edit/<int:pk>/', views.edit_exam, name='edit_exam'),
    path('delete/<int:pk>/', views.delete_exam, name='delete_exam'),
    path('results/<int:exam_id>/', views.exam_results, name='exam_results'),
    path('results/<int:exam_id>/add/', views.add_result, name='add_result'),
    path('results/edit/<int:pk>/', views.edit_result, name='edit_result'),
    path('results/delete/<int:pk>/', views.delete_result, name='delete_result'),
]
