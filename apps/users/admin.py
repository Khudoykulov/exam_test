from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentGroup, Notification


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'students_count', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at']
    raw_id_fields = ['user']


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'student_group', 'is_active']
    list_filter = ['user_type', 'is_active', 'is_staff', 'student_group', 'course']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Qo\'shimcha ma\'lumotlar', {
            'fields': ('user_type', 'phone', 'student_group', 'course', 'photo')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Qo\'shimcha ma\'lumotlar', {
            'fields': ('user_type', 'phone', 'student_group', 'course', 'photo')
        }),
    )
