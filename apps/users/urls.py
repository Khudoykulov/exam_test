from django.urls import path
from . import views
from apps.exams import views as exam_views

app_name = 'users'

urlpatterns = [
    path('', views.user_dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('profile/', views.user_profile, name='profile'),

    # Bildirishnomalar
    path('notifications/', exam_views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', exam_views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', exam_views.mark_all_notifications_read, name='mark_all_read'),
]
