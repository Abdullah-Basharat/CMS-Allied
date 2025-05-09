from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('students/', views.manage_students, name='manage_students'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:student_id>/update/', views.student_update, name='student_update'),
    path('students/<int:student_id>/delete/', views.student_delete, name='student_delete'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
]