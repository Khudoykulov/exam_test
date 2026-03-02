from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import models, IntegrityError
from .models import Exam, ExamAttempt, ExamAssignment, ExamGroupPermission, Subject
from apps.questions.models import Question, Answer
from apps.results.models import ExamResult
from apps.users.models import StudentGroup, CustomUser, Notification


def _get_student_exams(user):
    """Studentga ruxsat berilgan imtihonlarni qaytaradi"""
    now = timezone.now()
    if not user.student_group:
        return Exam.objects.none()

    # Faqat guruhga ruxsat berilgan va deadline o'tmagan imtihonlar
    permitted_exam_ids = ExamGroupPermission.objects.filter(
        group=user.student_group,
        is_active=True,
        deadline__gte=now
    ).values_list('exam_id', flat=True)

    return Exam.objects.filter(
        id__in=permitted_exam_ids,
        is_active=True,
        start_time__lte=now,
    ).select_related('subject', 'created_by')


@login_required
def exam_list(request):
    """Imtihonlar ro'yxati"""
    user = request.user
    now = timezone.now()

    if user.user_type == 'student':
        exams = _get_student_exams(user)
    elif user.user_type == 'teacher':
        # O'qituvchiga tayinlangan imtihonlar
        assigned_exam_ids = ExamAssignment.objects.filter(
            teacher=user,
            admin_deadline__gte=now
        ).values_list('exam_id', flat=True)
        exams = Exam.objects.filter(
            id__in=assigned_exam_ids,
            is_active=True,
        ).select_related('subject', 'created_by')
    else:
        # Adminlar uchun barcha imtihonlar
        exams = Exam.objects.filter(is_active=True).select_related('subject', 'created_by')

    context = {
        'exams': exams,
        'now': now
    }

    return render(request, 'exams/exam_list.html', context)


@login_required
def exam_detail(request, exam_id):
    """Imtihon tafsilotlari"""
    exam = get_object_or_404(Exam, id=exam_id)
    user = request.user
    now = timezone.now()
    permission = None

    # Student uchun ruxsat tekshiruvi
    if user.user_type == 'student':
        if not user.student_group:
            messages.error(request, "Siz hech qanday guruhga biriktirilmagansiz!")
            return redirect('exams:exam_list')
        permission = ExamGroupPermission.objects.filter(
            exam=exam,
            group=user.student_group,
            is_active=True,
            deadline__gte=now
        ).first()
        if not permission:
            messages.error(request, "Sizga bu imtihon uchun ruxsat berilmagan!")
            return redirect('exams:exam_list')
        if not exam.is_active or exam.start_time > now:
            messages.error(request, "Bu imtihon hozirda mavjud emas!")
            return redirect('exams:exam_list')
    elif user.user_type == 'teacher':
        # O'qituvchi faqat o'ziga tayinlangan imtihonlarni ko'ra oladi
        assignment = ExamAssignment.objects.filter(
            exam=exam,
            teacher=user
        ).first()
        if not assignment:
            messages.error(request, "Bu imtihon sizga tayinlanmagan!")
            return redirect('exams:exam_list')
    
    # Student ushbu imtihonni olganligini tekshirish
    attempt = ExamAttempt.objects.filter(
        exam=exam,
        student=request.user
    ).first()
    
    context = {
        'exam': exam,
        'attempt': attempt,
        'questions_count': exam.get_questions_count(),
        'permission': permission,
    }
    
    return render(request, 'exams/exam_detail.html', context)


@login_required
def start_exam(request, exam_id):
    """Imtihonni boshlash"""
    exam = get_object_or_404(Exam, id=exam_id)
    user = request.user
    now = timezone.now()

    # Faqat studentlar imtihon topshira oladi
    if user.user_type != 'student':
        messages.error(request, "Faqat studentlar imtihon topshira oladi!")
        return redirect('exams:exam_detail', exam_id=exam.id)

    # Ruxsat tekshiruvi
    if not user.student_group:
        messages.error(request, "Siz hech qanday guruhga biriktirilmagansiz!")
        return redirect('exams:exam_list')

    permission = ExamGroupPermission.objects.filter(
        exam=exam,
        group=user.student_group,
        is_active=True,
        deadline__gte=now
    ).first()
    if not permission:
        messages.error(request, "Sizga bu imtihon uchun ruxsat berilmagan yoki muddati o'tgan!")
        return redirect('exams:exam_list')

    if not exam.is_active or exam.start_time > now:
        messages.error(request, "Bu imtihon hozirda mavjud emas!")
        return redirect('exams:exam_list')
    
    # Avval imtihon topshirilganligini tekshirish
    attempt = ExamAttempt.objects.filter(
        exam=exam,
        student=request.user
    ).first()
    
    if attempt:
        if attempt.status == 'completed':
            messages.info(request, "Siz bu imtihonni allaqachon topshirgansiz!")
            result = ExamResult.objects.filter(attempt=attempt).first()
            if result:
                return redirect('results:result_detail', result_id=result.id)
            return redirect('results:result_list')
        else:
            messages.info(request, "Imtihonni davom ettiryapsiz...")
            return redirect('exams:take_exam', exam_id=exam.id)
    
    # Yangi urinish yaratish (race condition himoyasi)
    try:
        attempt = ExamAttempt.objects.create(
            exam=exam,
            student=request.user,
            status='in_progress'
        )
    except IntegrityError:
        attempt = ExamAttempt.objects.filter(
            exam=exam,
            student=request.user
        ).first()
        return redirect('exams:take_exam', exam_id=exam.id)
    
    messages.success(request, f"Imtihon boshlandi! Sizda {exam.duration} daqiqa vaqt bor.")
    return redirect('exams:take_exam', exam_id=exam.id)


@login_required
def take_exam(request, exam_id):
    """Imtihon topshirish"""
    exam = get_object_or_404(Exam, id=exam_id)
    
    # Urinishni topish
    attempt = get_object_or_404(
        ExamAttempt,
        exam=exam,
        student=request.user,
        status='in_progress'
    )
    
    # Vaqt tugaganligini tekshirish
    questions = exam.questions.all().prefetch_related('answers')
    time_passed = (timezone.now() - attempt.started_at).total_seconds() / 60
    time_expired = time_passed > exam.duration
    
    if time_expired and request.method == 'GET':
        # Vaqt tugagan — mavjud javoblar asosida avtomatik baholash
        result = _grade_exam(exam, attempt, questions, request)
        messages.error(request, "Vaqt tugadi! Imtihon avtomatik yakunlandi.")
        return redirect('results:result_detail', result_id=result.id)
    
    if request.method == 'POST':
        # Javoblarni saqlash va baholash
        result = _grade_exam(exam, attempt, questions, request)
        messages.success(request, f"Imtihon yakunlandi! Sizning balingiz: {result.score:.1f}")
        return redirect('results:result_detail', result_id=result.id)
    
    time_remaining = exam.duration - time_passed
    
    context = {
        'exam': exam,
        'attempt': attempt,
        'questions': questions,
        'time_remaining': int(time_remaining)
    }
    
    return render(request, 'exams/take_exam.html', context)


def _grade_exam(exam, attempt, questions, request):
    """Imtihonni baholash yordamchi funksiyasi"""
    correct_answers = 0
    wrong_answers = 0
    score = 0
    total_questions = questions.count()
    question_ids = list(questions.values_list('id', flat=True))

    for question in questions:
        selected_answer_id = request.POST.get(f'question_{question.id}')
        if selected_answer_id:
            # Javob haqiqiyligini va ushbu savol ga tegishliligini tekshirish
            selected_answer = Answer.objects.filter(
                id=selected_answer_id,
                question_id=question.id
            ).first()
            if selected_answer and selected_answer.is_correct:
                correct_answers += 1
                score += question.marks
            else:
                wrong_answers += 1
        # Javob berilmagan savollar hisoblalmaydi (skip)

    # Urinishni yakunlash
    attempt.status = 'completed'
    attempt.completed_at = timezone.now()
    attempt.save()

    # Natijani saqlash
    result = ExamResult.objects.create(
        exam=exam,
        student=attempt.student,
        attempt=attempt,
        score=score,
        total_questions=total_questions,
        correct_answers=correct_answers,
        wrong_answers=wrong_answers,
        passed=score >= exam.passing_marks
    )
    return result


@login_required
def my_exams(request):
    """Mening imtihonlarim"""
    attempts = ExamAttempt.objects.filter(
        student=request.user
    ).select_related('exam', 'exam__subject').order_by('-started_at')
    
    context = {
        'attempts': attempts
    }
    
    return render(request, 'exams/my_exams.html', context)


# ===== O'QITUVCHI VIEWS =====

@login_required
def teacher_dashboard(request):
    """O'qituvchi boshqaruv paneli"""
    user = request.user
    if user.user_type not in ('teacher', 'admin'):
        messages.error(request, "Sizga bu sahifaga kirishga ruxsat yo'q!")
        return redirect('users:dashboard')

    now = timezone.now()

    # O'qituvchiga tayinlangan imtihonlar
    assignments = ExamAssignment.objects.filter(
        teacher=user
    ).select_related('exam', 'exam__subject', 'assigned_by').order_by('-created_at')

    # Guruh ruxsatlari
    permissions = ExamGroupPermission.objects.filter(
        teacher=user
    ).select_related('exam', 'exam__subject', 'group').order_by('-created_at')

    context = {
        'assignments': assignments,
        'permissions': permissions,
        'now': now,
    }
    return render(request, 'exams/teacher_dashboard.html', context)


@login_required
def grant_permission(request, assignment_id):
    """O'qituvchi guruhga imtihon uchun ruxsat beradi"""
    user = request.user
    if user.user_type not in ('teacher', 'admin'):
        messages.error(request, "Sizga bu sahifaga kirishga ruxsat yo'q!")
        return redirect('users:dashboard')

    assignment = get_object_or_404(ExamAssignment, id=assignment_id, teacher=user)
    now = timezone.now()

    # Admin deadline tekshiruvi
    if now > assignment.admin_deadline:
        messages.error(request, "Admin belgilagan muddat o'tib ketgan!")
        return redirect('exams:teacher_dashboard')

    # Admin start time tekshiruvi
    if assignment.admin_start_time and now < assignment.admin_start_time:
        messages.error(request, f"Ruxsat berish {assignment.admin_start_time.strftime('%d.%m.%Y %H:%M')} dan boshlab mumkin!")
        return redirect('exams:teacher_dashboard')

    groups = StudentGroup.objects.all()

    # Allaqachon ruxsat berilgan guruhlar
    existing_permissions = ExamGroupPermission.objects.filter(
        exam=assignment.exam,
        teacher=user
    ).select_related('group')
    existing_group_ids = set(existing_permissions.values_list('group_id', flat=True))

    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        deadline_str = request.POST.get('deadline')

        if not deadline_str:
            messages.error(request, "Deadline tanlanishi shart!")
            return redirect('exams:grant_permission', assignment_id=assignment.id)

        # Deadline parsing
        from datetime import datetime
        try:
            deadline = timezone.make_aware(datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M'))
        except (ValueError, TypeError):
            messages.error(request, "Deadline formati noto'g'ri!")
            return redirect('exams:grant_permission', assignment_id=assignment.id)

        # Admin deadline'dan oshmasligi
        if deadline > assignment.admin_deadline:
            messages.error(request, f"Deadline admin muddatidan ({assignment.admin_deadline.strftime('%d.%m.%Y %H:%M')}) oshmasligi kerak!")
            return redirect('exams:grant_permission', assignment_id=assignment.id)

        # "Barcha guruhlar" tanlangan bo'lsa
        if group_id == 'all':
            target_groups = groups
            created_count = 0
            updated_count = 0
            for g in target_groups:
                perm, created = ExamGroupPermission.objects.update_or_create(
                    exam=assignment.exam,
                    group=g,
                    defaults={
                        'teacher': user,
                        'deadline': deadline,
                        'is_active': True,
                    }
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1
            msg_parts = []
            if created_count:
                msg_parts.append(f"{created_count} ta guruhga ruxsat berildi")
            if updated_count:
                msg_parts.append(f"{updated_count} ta guruh yangilandi")
            messages.success(request, f"Barcha guruhlar uchun '{assignment.exam.title}': {', '.join(msg_parts)}!")
        else:
            if not group_id:
                messages.error(request, "Guruh tanlanishi shart!")
                return redirect('exams:grant_permission', assignment_id=assignment.id)

            group = get_object_or_404(StudentGroup, id=group_id)

            # Yaratish yoki yangilash
            perm, created = ExamGroupPermission.objects.update_or_create(
                exam=assignment.exam,
                group=group,
                defaults={
                    'teacher': user,
                    'deadline': deadline,
                    'is_active': True,
                }
            )

            if created:
                messages.success(request, f"'{group.name}' guruhiga '{assignment.exam.title}' imtihoni uchun ruxsat berildi!")
            else:
                messages.success(request, f"'{group.name}' guruhi uchun ruxsat yangilandi!")

        return redirect('exams:teacher_dashboard')

    context = {
        'assignment': assignment,
        'groups': groups,
        'existing_permissions': existing_permissions,
        'existing_group_ids': existing_group_ids,
    }
    return render(request, 'exams/grant_permission.html', context)


@login_required
def revoke_permission(request, permission_id):
    """O'qituvchi guruh ruxsatini bekor qiladi"""
    user = request.user
    if user.user_type not in ('teacher', 'admin'):
        messages.error(request, "Sizga ruxsat yo'q!")
        return redirect('users:dashboard')

    perm = get_object_or_404(ExamGroupPermission, id=permission_id, teacher=user)
    group_name = perm.group.name
    exam_title = perm.exam.title
    perm.is_active = False
    perm.save()
    messages.success(request, f"'{group_name}' guruhi uchun '{exam_title}' imtihon ruxsati bekor qilindi!")
    return redirect('exams:teacher_dashboard')


@login_required
def teacher_results(request, exam_id):
    """O'qituvchi imtihon natijalarini ko'rish"""
    user = request.user
    if user.user_type not in ('teacher', 'admin'):
        messages.error(request, "Sizga ruxsat yo'q!")
        return redirect('users:dashboard')

    exam = get_object_or_404(Exam, id=exam_id)

    # O'qituvchiga tayinlanganligini tekshirish
    if user.user_type == 'teacher':
        assignment = ExamAssignment.objects.filter(exam=exam, teacher=user).first()
        if not assignment:
            messages.error(request, "Bu imtihon sizga tayinlanmagan!")
            return redirect('exams:teacher_dashboard')

    results = ExamResult.objects.filter(
        exam=exam
    ).select_related('student', 'student__student_group').order_by('-score')

    context = {
        'exam': exam,
        'results': results,
    }
    return render(request, 'exams/teacher_results.html', context)


# ===== ADMIN RUXSAT BERISH VIEWS =====

@login_required
def admin_assignments(request):
    """Admin sahifasi — imtihonlarni o'qituvchilarga tayinlash"""
    user = request.user
    if user.user_type != 'admin' and not user.is_superuser:
        messages.error(request, "Faqat administratorlar uchun!")
        return redirect('users:dashboard')

    now = timezone.now()

    # Fanlar bo'yicha o'qituvchilar va ularning tayinlanishlari
    subjects = Subject.objects.all()
    teachers = CustomUser.objects.filter(user_type='teacher').order_by('first_name', 'last_name')
    exams = Exam.objects.filter(is_active=True).select_related('subject').order_by('subject__name', 'title')

    # Mavjud tayinlanishlar
    assignments = ExamAssignment.objects.select_related(
        'exam', 'exam__subject', 'teacher', 'assigned_by'
    ).order_by('exam__subject__name', 'teacher__first_name')

    # Filtrlash
    selected_subject = request.GET.get('subject', '')
    if selected_subject:
        assignments = assignments.filter(exam__subject_id=selected_subject)
        exams = exams.filter(subject_id=selected_subject)

    context = {
        'subjects': subjects,
        'teachers': teachers,
        'exams': exams,
        'assignments': assignments,
        'now': now,
        'selected_subject': selected_subject,
    }
    return render(request, 'exams/admin_assignments.html', context)


@login_required
def admin_create_assignment(request):
    """Admin — yangi tayinlanish yaratish"""
    user = request.user
    if user.user_type != 'admin' and not user.is_superuser:
        messages.error(request, "Faqat administratorlar uchun!")
        return redirect('users:dashboard')

    if request.method != 'POST':
        return redirect('exams:admin_assignments')

    exam_id = request.POST.get('exam_id')
    teacher_id = request.POST.get('teacher_id')
    start_time_str = request.POST.get('start_time', '').strip()
    deadline_str = request.POST.get('deadline', '').strip()

    if not exam_id or not teacher_id or not deadline_str:
        messages.error(request, "Imtihon, o'qituvchi va tugash vaqti tanlanishi shart!")
        return redirect('exams:admin_assignments')

    exam = get_object_or_404(Exam, id=exam_id)
    teacher = get_object_or_404(CustomUser, id=teacher_id, user_type='teacher')

    from datetime import datetime
    try:
        admin_deadline = timezone.make_aware(datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M'))
    except (ValueError, TypeError):
        messages.error(request, "Tugash vaqti formati noto'g'ri!")
        return redirect('exams:admin_assignments')

    admin_start_time = None
    if start_time_str:
        try:
            admin_start_time = timezone.make_aware(datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M'))
        except (ValueError, TypeError):
            messages.error(request, "Boshlanish vaqti formati noto'g'ri!")
            return redirect('exams:admin_assignments')

    if admin_start_time and admin_start_time >= admin_deadline:
        messages.error(request, "Boshlanish vaqti tugash vaqtidan oldin bo'lishi kerak!")
        return redirect('exams:admin_assignments')

    # Yaratish yoki yangilash
    assignment, created = ExamAssignment.objects.update_or_create(
        exam=exam,
        teacher=teacher,
        defaults={
            'admin_start_time': admin_start_time,
            'admin_deadline': admin_deadline,
            'assigned_by': user,
        }
    )

    # O'qituvchiga bildirishnoma yuborish
    start_info = ''
    if admin_start_time:
        start_info = f"Boshlanish: {admin_start_time.strftime('%d.%m.%Y %H:%M')}\n"

    Notification.objects.create(
        user=teacher,
        notification_type='assignment',
        title=f"Yangi imtihon tayinlandi: {exam.title}",
        message=(
            f"Sizga \"{exam.title}\" ({exam.subject.name}) imtihoni tayinlandi.\n"
            f"{start_info}"
            f"Tugash muddati: {admin_deadline.strftime('%d.%m.%Y %H:%M')}\n"
            f"Tayinlagan: {user.get_full_name()}\n\n"
            f"O'qituvchi boshqaruv panelidan guruhlarni tanlashingiz va ruxsat berishingiz mumkin."
        )
    )

    action = "tayinlandi" if created else "yangilandi"
    messages.success(
        request,
        f"'{exam.title}' imtihoni {teacher.get_full_name()} ga {action}! "
        f"O'qituvchiga bildirishnoma yuborildi."
    )
    return redirect('exams:admin_assignments')


@login_required
def admin_delete_assignment(request, assignment_id):
    """Admin — tayinlanishni o'chirish"""
    user = request.user
    if user.user_type != 'admin' and not user.is_superuser:
        messages.error(request, "Faqat administratorlar uchun!")
        return redirect('users:dashboard')

    assignment = get_object_or_404(ExamAssignment, id=assignment_id)
    teacher = assignment.teacher
    exam_title = assignment.exam.title

    # O'qituvchiga bildirishnoma
    Notification.objects.create(
        user=teacher,
        notification_type='info',
        title=f"Imtihon tayinlanishi bekor qilindi",
        message=(
            f"\"{exam_title}\" imtihoni uchun tayinlanishingiz "
            f"administrator ({user.get_full_name()}) tomonidan bekor qilindi."
        )
    )

    assignment.delete()
    messages.success(request, f"'{exam_title}' tayinlanishi o'chirildi. O'qituvchiga xabar yuborildi.")
    return redirect('exams:admin_assignments')


# ===== BILDIRISHNOMALAR =====

@login_required
def notifications(request):
    """Foydalanuvchi bildirishnomalari"""
    user_notifications = request.user.notifications.all()[:50]
    unread_count = request.user.notifications.filter(is_read=False).count()

    context = {
        'notifications': user_notifications,
        'unread_count': unread_count,
    }
    return render(request, 'users/notifications.html', context)


@login_required
def mark_notification_read(request, notification_id):
    """Bildirishnomani o'qilgan deb belgilash"""
    notification = get_object_or_404(
        Notification, id=notification_id, user=request.user
    )
    notification.is_read = True
    notification.save()
    return redirect('users:notifications')


@login_required
def mark_all_notifications_read(request):
    """Barcha bildirishnomalarni o'qilgan deb belgilash"""
    request.user.notifications.filter(is_read=False).update(is_read=True)
    messages.success(request, "Barcha bildirishnomalar o'qilgan deb belgilandi.")
    return redirect('users:notifications')
