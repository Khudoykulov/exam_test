from django.contrib.auth.models import AbstractUser
from django.db import models


class StudentGroup(models.Model):
    """Talabalar guruhi"""
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Guruh nomi'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Tavsif'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan vaqti'
    )

    class Meta:
        verbose_name = 'Guruh'
        verbose_name_plural = 'Guruhlar'
        ordering = ['name']

    def __str__(self):
        return self.name

    def students_count(self):
        return self.students.count()


class CustomUser(AbstractUser):
    """Custom User Model"""
    
    USER_TYPES = (
        ('student', 'Student'),
        ('teacher', 'O\'qituvchi'),
        ('admin', 'Administrator'),
    )
    
    user_type = models.CharField(
        max_length=20, 
        choices=USER_TYPES, 
        default='student',
        verbose_name='Foydalanuvchi turi'
    )
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name='Telefon raqami'
    )
    student_group = models.ForeignKey(
        StudentGroup,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='students',
        verbose_name='Guruh'
    )
    # Eski group maydoni — migratsiya uchun saqlab qolamiz
    group = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name='Guruh (eski)'
    )
    course = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name='Kurs'
    )
    photo = models.ImageField(
        upload_to='users/photos/', 
        blank=True, 
        null=True,
        verbose_name='Fotosurat'
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
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
    
    def get_full_name(self):
        """Foydalanuvchining to'liq ismini qaytaradi"""
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def get_group_name(self):
        """Guruh nomini qaytaradi"""
        if self.student_group:
            return self.student_group.name
        return self.group or ''

    def unread_notifications_count(self):
        return self.notifications.filter(is_read=False).count()


class Notification(models.Model):
    """Bildirishnoma modeli"""
    NOTIFICATION_TYPES = (
        ('assignment', 'Imtihon tayinlandi'),
        ('permission', 'Ruxsat berildi'),
        ('info', 'Ma\'lumot'),
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Foydalanuvchi'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='info',
        verbose_name='Turi'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Sarlavha'
    )
    message = models.TextField(
        verbose_name='Xabar'
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='O\'qilgan'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan vaqti'
    )

    class Meta:
        verbose_name = 'Bildirishnoma'
        verbose_name_plural = 'Bildirishnomalar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} → {self.user.get_full_name()}"
