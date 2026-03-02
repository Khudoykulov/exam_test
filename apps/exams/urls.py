from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('<int:exam_id>/', views.exam_detail, name='exam_detail'),
    path('<int:exam_id>/start/', views.start_exam, name='start_exam'),
    path('<int:exam_id>/take/', views.take_exam, name='take_exam'),
    path('my-exams/', views.my_exams, name='my_exams'),

    # O'qituvchi sahifalari
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/grant/<int:assignment_id>/', views.grant_permission, name='grant_permission'),
    path('teacher/revoke/<int:permission_id>/', views.revoke_permission, name='revoke_permission'),
    path('teacher/results/<int:exam_id>/', views.teacher_results, name='teacher_results'),

    # Admin ruxsat berish sahifalari
    path('admin-panel/assignments/', views.admin_assignments, name='admin_assignments'),
    path('admin-panel/assignments/create/', views.admin_create_assignment, name='admin_create_assignment'),
    path('admin-panel/assignments/delete/<int:assignment_id>/', views.admin_delete_assignment, name='admin_delete_assignment'),
]
