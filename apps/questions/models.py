from django.db import models
from apps.exams.models import Exam


class Question(models.Model):
    """Savol modeli"""
    
    DIFFICULTY_CHOICES = (
        ('easy', 'Oson'),
        ('medium', 'O\'rta'),
        ('hard', 'Qiyin'),
    )
    
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Imtihon'
    )
    question_text = models.TextField(verbose_name='Savol matni')
    question_image = models.ImageField(
        upload_to='questions/',
        blank=True,
        null=True,
        verbose_name='Savol rasmi'
    )
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='medium',
        verbose_name='Qiyinlik darajasi'
    )
    marks = models.IntegerField(
        default=1,
        verbose_name='Ball'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='Tartib raqami'
    )
    explanation = models.TextField(
        blank=True,
        verbose_name='Tushuntirish'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan vaqti'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Yangilangan vaqti'
    )
    
    class Meta:
        verbose_name = 'Savol'
        verbose_name_plural = 'Savollar'
        ordering = ['exam', 'order']
    
    def __str__(self):
        return f"{self.exam.title} - Q{self.order}"
    
    def get_correct_answer(self):
        """To'g'ri javobni qaytaradi"""
        return self.answers.filter(is_correct=True).first()


class Answer(models.Model):
    """Javob modeli"""
    
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Savol'
    )
    answer_text = models.TextField(verbose_name='Javob matni')
    answer_image = models.ImageField(
        upload_to='answers/',
        blank=True,
        null=True,
        verbose_name='Javob rasmi'
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name='To\'g\'ri javob'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='Tartib raqami'
    )
    
    class Meta:
        verbose_name = 'Javob'
        verbose_name_plural = 'Javoblar'
        ordering = ['question', 'order']
    
    def __str__(self):
        status = "✓" if self.is_correct else "✗"
        return f"{status} {self.answer_text[:50]}"
