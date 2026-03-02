from django.contrib import admin
from .models import Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    fields = ['answer_text', 'is_correct', 'order']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'exam', 'difficulty', 'marks', 'order']
    list_filter = ['exam', 'difficulty']
    search_fields = ['question_text', 'exam__title']
    inlines = [AnswerInline]
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('exam', 'question_text', 'question_image')
        }),
        ('Sozlamalar', {
            'fields': ('difficulty', 'marks', 'order', 'explanation')
        }),
    )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'question', 'is_correct']
    list_filter = ['is_correct', 'question__exam']
    search_fields = ['answer_text', 'question__question_text']
