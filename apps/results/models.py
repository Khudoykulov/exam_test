from django.db import models
from django.conf import settings
from apps.exams.models import Exam, ExamAttempt


class ExamResult(models.Model):
    """Imtihon natijasi modeli"""
    
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='Imtihon'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='exam_results',
        verbose_name='Student'
    )
    attempt = models.OneToOneField(
        ExamAttempt,
        on_delete=models.CASCADE,
        related_name='result',
        verbose_name='Urinish'
    )
    score = models.FloatField(verbose_name='Ball')
    percentage = models.FloatField(
        default=0,
        verbose_name='Foiz'
    )
    total_questions = models.IntegerField(
        verbose_name='Jami savollar'
    )
    correct_answers = models.IntegerField(
        verbose_name='To\'g\'ri javoblar'
    )
    wrong_answers = models.IntegerField(
        verbose_name='Noto\'g\'ri javoblar'
    )
    passed = models.BooleanField(
        default=False,
        verbose_name='O\'tdi'
    )
    feedback = models.TextField(
        blank=True,
        verbose_name='Fikr-mulohaza'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan vaqti'
    )
    
    class Meta:
        verbose_name = 'Natija'
        verbose_name_plural = 'Natijalar'
        ordering = ['-created_at']
        unique_together = ['exam', 'student']
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.exam.title} ({self.score})"
    
    def save(self, *args, **kwargs):
        """Foizni hisoblash"""
        if self.exam.total_marks > 0:
            self.percentage = (self.score / self.exam.total_marks) * 100
        super().save(*args, **kwargs)
    
    def get_grade(self):
        """Bahoni olish"""
        if self.percentage >= 90:
            return 'A'
        elif self.percentage >= 80:
            return 'B'
        elif self.percentage >= 70:
            return 'C'
        elif self.percentage >= 60:
            return 'D'
        else:
            return 'F'
