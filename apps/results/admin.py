from django.contrib import admin
from .models import ExamResult


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'score', 'percentage', 'passed', 'created_at']
    list_filter = ['passed', 'exam', 'created_at']
    search_fields = ['student__username', 'student__first_name', 'student__last_name', 'exam__title']
    date_hierarchy = 'created_at'
    readonly_fields = ['percentage', 'created_at']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('exam', 'student', 'attempt')
        }),
        ('Natija', {
            'fields': ('score', 'percentage', 'total_questions', 'correct_answers', 'wrong_answers', 'passed')
        }),
        ('Qo\'shimcha', {
            'fields': ('feedback', 'created_at')
        }),
    )
