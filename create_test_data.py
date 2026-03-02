"""
Test ma'lumotlarini yaratish skripti
Oraliq va yakuniy nazorat uchun namuna testlar
"""
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from django.utils import timezone
from datetime import timedelta
from apps.users.models import CustomUser, StudentGroup
from apps.exams.models import Subject, Exam, ExamAttempt, ExamAssignment, ExamGroupPermission
from apps.questions.models import Question, Answer


def create_test_data():
    # ===== GURUHLAR =====
    group_it21, _ = StudentGroup.objects.get_or_create(
        name='IT-21',
        defaults={'description': 'Informatika texnologiyalari, 2-kurs 1-guruh'}
    )
    group_it22, _ = StudentGroup.objects.get_or_create(
        name='IT-22',
        defaults={'description': 'Informatika texnologiyalari, 2-kurs 2-guruh'}
    )
    group_mt31, _ = StudentGroup.objects.get_or_create(
        name='MT-31',
        defaults={'description': 'Matematika, 3-kurs 1-guruh'}
    )
    print(f"✅ 3 ta guruh yaratildi: IT-21, IT-22, MT-31")

    # ===== FANLAR =====
    subjects = [
        Subject.objects.get_or_create(name='Informatika', defaults={'description': 'Informatika asoslari va dasturlash'})[0],
        Subject.objects.get_or_create(name='Matematika', defaults={'description': 'Oliy matematika'})[0],
        Subject.objects.get_or_create(name='Fizika', defaults={'description': 'Umumiy fizika'})[0],
    ]
    print(f"✅ {len(subjects)} ta fan yaratildi")

    # ===== O'QITUVCHI =====
    teacher, created = CustomUser.objects.get_or_create(
        username='teacher1',
        defaults={
            'first_name': 'Ahror',
            'last_name': 'Karimov',
            'email': 'teacher@example.com',
            'user_type': 'teacher',
        }
    )
    if created:
        teacher.set_password('teacher123')
        teacher.save()
    print(f"✅ O'qituvchi: teacher1 / teacher123")

    # ===== STUDENTLAR =====
    student, created = CustomUser.objects.get_or_create(
        username='student1',
        defaults={
            'first_name': 'Ali',
            'last_name': 'Valiyev',
            'email': 'student@example.com',
            'user_type': 'student',
            'student_group': group_it21,
            'course': 2,
        }
    )
    if created:
        student.set_password('student123')
        student.save()
    else:
        # Eski student guruhga biriktirish
        if not student.student_group:
            student.student_group = group_it21
            student.save()
    print(f"✅ Student: student1 / student123 (guruh: IT-21)")

    student2, created = CustomUser.objects.get_or_create(
        username='student2',
        defaults={
            'first_name': 'Sarvar',
            'last_name': 'Toshmatov',
            'email': 'student2@example.com',
            'user_type': 'student',
            'student_group': group_it22,
            'course': 2,
        }
    )
    if created:
        student2.set_password('student123')
        student2.save()
    print(f"✅ Student: student2 / student123 (guruh: IT-22)")

    now = timezone.now()

    # ===== ORALIQ NAZORAT - INFORMATIKA =====
    exam1, _ = Exam.objects.get_or_create(
        title='Informatika - Oraliq nazorat',
        defaults={
            'subject': subjects[0],
            'exam_type': 'midterm',
            'description': 'Informatika fanidan oraliq nazorat testi. Dasturlash asoslari, algoritmlar va ma\'lumotlar tuzilmasi bo\'yicha savollar.',
            'duration': 45,
            'total_marks': 100,
            'passing_marks': 55,
            'start_time': now - timedelta(days=1),
            'end_time': now + timedelta(days=30),
            'is_active': True,
            'created_by': teacher,
            'allowed_groups': '',
        }
    )

    # Informatika savollari
    informatika_questions = [
        {
            'text': 'Python dasturlash tilida list (ro\'yxat) yaratish uchun qaysi belgi ishlatiladi?',
            'answers': [
                ('{ }', False),
                ('[ ]', True),
                ('( )', False),
                ('< >', False),
            ]
        },
        {
            'text': 'Quyidagilardan qaysi biri Python\'da to\'g\'ri o\'zgaruvchi nomi hisoblanadi?',
            'answers': [
                ('2variable', False),
                ('my-var', False),
                ('my_variable', True),
                ('class', False),
            ]
        },
        {
            'text': 'SQL da ma\'lumotlar bazasidan ma\'lumot olish uchun qaysi kalit so\'z ishlatiladi?',
            'answers': [
                ('GET', False),
                ('FETCH', False),
                ('SELECT', True),
                ('RETRIEVE', False),
            ]
        },
        {
            'text': 'HTML da sarlavha yaratish uchun qaysi teg ishlatiladi?',
            'answers': [
                ('<header>', False),
                ('<h1>', True),
                ('<title>', False),
                ('<head>', False),
            ]
        },
        {
            'text': 'Quyidagi kodning natijasi nima bo\'ladi?\n\nprint(type(10.5))',
            'answers': [
                ("<class 'int'>", False),
                ("<class 'float'>", True),
                ("<class 'str'>", False),
                ("<class 'double'>", False),
            ]
        },
        {
            'text': 'Git versiya boshqaruv tizimida yangi branch yaratish uchun qaysi buyruq ishlatiladi?',
            'answers': [
                ('git new branch', False),
                ('git branch -create', False),
                ('git checkout -b', True),
                ('git make branch', False),
            ]
        },
        {
            'text': 'CSS da elementning foniga rang berish uchun qaysi xususiyat ishlatiladi?',
            'answers': [
                ('color', False),
                ('background-color', True),
                ('font-color', False),
                ('bg-color', False),
            ]
        },
        {
            'text': 'Python\'da for tsikli qanday ishlaydi?',
            'answers': [
                ('Faqat raqamlar uchun ishlaydi', False),
                ('Iterable (takrorlanadigan) ob\'yektlar ustida ishlaydi', True),
                ('Faqat stringlar uchun ishlaydi', False),
                ('Faqat dictionary uchun ishlaydi', False),
            ]
        },
        {
            'text': 'HTTP so\'rov metodlaridan qaysi biri ma\'lumot yaratish uchun ishlatiladi?',
            'answers': [
                ('GET', False),
                ('POST', True),
                ('DELETE', False),
                ('HEAD', False),
            ]
        },
        {
            'text': 'Django framework\'da URL marshrutlash (routing) qaysi faylda sozlanadi?',
            'answers': [
                ('views.py', False),
                ('models.py', False),
                ('urls.py', True),
                ('settings.py', False),
            ]
        },
    ]

    for i, q_data in enumerate(informatika_questions, 1):
        question, _ = Question.objects.get_or_create(
            exam=exam1,
            question_text=q_data['text'],
            defaults={
                'difficulty': 'medium',
                'marks': 10,
                'order': i,
            }
        )
        for j, (ans_text, is_correct) in enumerate(q_data['answers'], 1):
            Answer.objects.get_or_create(
                question=question,
                answer_text=ans_text,
                defaults={'is_correct': is_correct, 'order': j}
            )
    print(f"✅ Informatika oraliq nazorat - {len(informatika_questions)} ta savol yaratildi")

    # ===== YAKUNIY NAZORAT - INFORMATIKA =====
    exam2, _ = Exam.objects.get_or_create(
        title='Informatika - Yakuniy nazorat',
        defaults={
            'subject': subjects[0],
            'exam_type': 'final',
            'description': 'Informatika fanidan yakuniy nazorat testi. Butun semestr materiallarini qamrab oladi.',
            'duration': 60,
            'total_marks': 100,
            'passing_marks': 55,
            'start_time': now - timedelta(days=1),
            'end_time': now + timedelta(days=30),
            'is_active': True,
            'created_by': teacher,
            'allowed_groups': '',
        }
    )

    informatika_final_questions = [
        {
            'text': 'OOP (Ob\'yektga yo\'naltirilgan dasturlash) ning asosiy tamoyillari qaysilar?',
            'answers': [
                ('Loop, Condition, Function, Variable', False),
                ('Encapsulation, Inheritance, Polymorphism, Abstraction', True),
                ('Input, Output, Process, Storage', False),
                ('HTML, CSS, JS, SQL', False),
            ]
        },
        {
            'text': 'Python\'da dictionary (lug\'at) ma\'lumot turida kalit (key) sifatida qaysi turlardan foydalanish mumkin?',
            'answers': [
                ('Faqat stringlar', False),
                ('Faqat sonlar', False),
                ('Har qanday o\'zgarmas (immutable) turlar', True),
                ('Faqat tuple', False),
            ]
        },
        {
            'text': 'Django ORM da barcha ob\'yektlarni olish uchun qaysi metod ishlatiladi?',
            'answers': [
                ('Model.get_all()', False),
                ('Model.objects.all()', True),
                ('Model.fetch_all()', False),
                ('Model.select_all()', False),
            ]
        },
        {
            'text': 'REST API da 404 status kodi nimani bildiradi?',
            'answers': [
                ('Server xatosi', False),
                ('So\'rov muvaffaqiyatli', False),
                ('Resurs topilmadi', True),
                ('Ruxsat yo\'q', False),
            ]
        },
        {
            'text': 'Python\'da decorator nima vazifa bajaradi?',
            'answers': [
                ('O\'zgaruvchilarni saqlaydi', False),
                ('Funksiyani o\'zgartirmasdan unga qo\'shimcha funksionallik qo\'shadi', True),
                ('Ma\'lumotlar bazasiga ulanadi', False),
                ('Fayllarni o\'qiydi', False),
            ]
        },
        {
            'text': 'SQL da jadvallarni birlashtirish uchun qaysi kalit so\'z ishlatiladi?',
            'answers': [
                ('MERGE', False),
                ('COMBINE', False),
                ('JOIN', True),
                ('CONNECT', False),
            ]
        },
        {
            'text': 'Git da oxirgi commitni bekor qilish uchun qaysi buyruq ishlatiladi?',
            'answers': [
                ('git undo', False),
                ('git revert HEAD', True),
                ('git cancel', False),
                ('git remove last', False),
            ]
        },
        {
            'text': 'Python\'da xatolikni ushlash uchun qaysi konstruktsiya ishlatiladi?',
            'answers': [
                ('if-else', False),
                ('try-except', True),
                ('for-in', False),
                ('while-do', False),
            ]
        },
        {
            'text': 'Django\'da template tizimida o\'zgaruvchini chiqarish uchun qaysi sintaksis ishlatiladi?',
            'answers': [
                ('{% variable %}', False),
                ('{{ variable }}', True),
                ('[% variable %]', False),
                ('<% variable %>', False),
            ]
        },
        {
            'text': 'HTTP va HTTPS orasidagi asosiy farq nima?',
            'answers': [
                ('Tezlik farqi', False),
                ('HTTPS shifrlangan (SSL/TLS) aloqa ishlatadi', True),
                ('HTTP yangi versiya', False),
                ('Farq yo\'q', False),
            ]
        },
    ]

    for i, q_data in enumerate(informatika_final_questions, 1):
        question, _ = Question.objects.get_or_create(
            exam=exam2,
            question_text=q_data['text'],
            defaults={
                'difficulty': 'hard',
                'marks': 10,
                'order': i,
            }
        )
        for j, (ans_text, is_correct) in enumerate(q_data['answers'], 1):
            Answer.objects.get_or_create(
                question=question,
                answer_text=ans_text,
                defaults={'is_correct': is_correct, 'order': j}
            )
    print(f"✅ Informatika yakuniy nazorat - {len(informatika_final_questions)} ta savol yaratildi")

    # ===== ORALIQ NAZORAT - MATEMATIKA =====
    exam3, _ = Exam.objects.get_or_create(
        title='Matematika - Oraliq nazorat',
        defaults={
            'subject': subjects[1],
            'exam_type': 'midterm',
            'description': 'Matematika fanidan oraliq nazorat testi. Chiziqli algebra va matematik analiz asoslari.',
            'duration': 40,
            'total_marks': 100,
            'passing_marks': 55,
            'start_time': now - timedelta(days=1),
            'end_time': now + timedelta(days=30),
            'is_active': True,
            'created_by': teacher,
            'allowed_groups': '',
        }
    )

    matematika_questions = [
        {
            'text': '2x + 5 = 15 tenglamaning yechimi nima?',
            'answers': [
                ('x = 3', False),
                ('x = 5', True),
                ('x = 7', False),
                ('x = 10', False),
            ]
        },
        {
            'text': 'Matritsa ko\'paytirish uchun qanday shart bajarilishi kerak?',
            'answers': [
                ('Matritsalar bir xil o\'lchamda bo\'lishi kerak', False),
                ('Birinchi matritsaning ustunlar soni ikkinchisining qatorlar soniga teng bo\'lishi kerak', True),
                ('Ikkala matritsa kvadrat bo\'lishi kerak', False),
                ('Hech qanday shart yo\'q', False),
            ]
        },
        {
            'text': 'f(x) = x² funksiyaning hosilasi (derivative) nima?',
            'answers': [
                ("f'(x) = x", False),
                ("f'(x) = 2x", True),
                ("f'(x) = x²", False),
                ("f'(x) = 2", False),
            ]
        },
        {
            'text': '∫ 2x dx integrali nima?',
            'answers': [
                ('x + C', False),
                ('x² + C', True),
                ('2x² + C', False),
                ('x³ + C', False),
            ]
        },
        {
            'text': 'Determinant 0 ga teng bo\'lgan matritsa qanday deyiladi?',
            'answers': [
                ('Birlik matritsa', False),
                ('Singulyar (degenerat) matritsa', True),
                ('Diagonal matritsa', False),
                ('Simmetrik matritsa', False),
            ]
        },
    ]

    for i, q_data in enumerate(matematika_questions, 1):
        question, _ = Question.objects.get_or_create(
            exam=exam3,
            question_text=q_data['text'],
            defaults={
                'difficulty': 'medium',
                'marks': 20,
                'order': i,
            }
        )
        for j, (ans_text, is_correct) in enumerate(q_data['answers'], 1):
            Answer.objects.get_or_create(
                question=question,
                answer_text=ans_text,
                defaults={'is_correct': is_correct, 'order': j}
            )
    print(f"✅ Matematika oraliq nazorat - {len(matematika_questions)} ta savol yaratildi")

    # ===== ADMIN FOYDALANUVCHI =====
    admin_user = CustomUser.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = CustomUser.objects.filter(user_type='admin').first()

    # ===== IMTIHON TAYINLASHLARI (Admin → O'qituvchi) =====
    if admin_user:
        assignment1, _ = ExamAssignment.objects.get_or_create(
            exam=exam1,
            teacher=teacher,
            defaults={
                'admin_deadline': now + timedelta(days=25),
                'assigned_by': admin_user,
            }
        )
        assignment2, _ = ExamAssignment.objects.get_or_create(
            exam=exam2,
            teacher=teacher,
            defaults={
                'admin_deadline': now + timedelta(days=30),
                'assigned_by': admin_user,
            }
        )
        assignment3, _ = ExamAssignment.objects.get_or_create(
            exam=exam3,
            teacher=teacher,
            defaults={
                'admin_deadline': now + timedelta(days=20),
                'assigned_by': admin_user,
            }
        )
        print(f"✅ 3 ta imtihon teacher1 ga tayinlandi (admin tomonidan)")

        # ===== GURUH RUXSATLARI (O'qituvchi → Guruh) =====
        perm1, _ = ExamGroupPermission.objects.get_or_create(
            exam=exam1,
            group=group_it21,
            defaults={
                'teacher': teacher,
                'deadline': now + timedelta(days=20),
                'is_active': True,
            }
        )
        perm2, _ = ExamGroupPermission.objects.get_or_create(
            exam=exam2,
            group=group_it21,
            defaults={
                'teacher': teacher,
                'deadline': now + timedelta(days=25),
                'is_active': True,
            }
        )
        # IT-22 guruhga faqat birinchi imtihonga ruxsat
        perm3, _ = ExamGroupPermission.objects.get_or_create(
            exam=exam1,
            group=group_it22,
            defaults={
                'teacher': teacher,
                'deadline': now + timedelta(days=15),
                'is_active': True,
            }
        )
        print(f"✅ Guruh ruxsatlari berildi:")
        print(f"   IT-21 → Informatika oraliq, yakuniy")
        print(f"   IT-22 → Informatika oraliq")
        print(f"   MT-31 → hech qanday ruxsat yo'q (ko'ra olmaydi)")
    else:
        print("⚠️  Admin foydalanuvchi topilmadi — ExamAssignment yaratilmadi")
        print("   Avval admin yarating va create_test_data.py ni qayta ishga tushiring")

    print("\n" + "=" * 50)
    print("✅ Barcha test ma'lumotlari muvaffaqiyatli yaratildi!")
    print("=" * 50)
    print("\n📋 Foydalanuvchilar:")
    print("   Admin:     admin / admin123")
    print("   O'qituvchi: teacher1 / teacher123")
    print("   Student 1: student1 / student123  (guruh: IT-21)")
    print("   Student 2: student2 / student123  (guruh: IT-22)")
    print("\n📋 Guruhlar: IT-21, IT-22, MT-31")
    print("\n📋 Imtihonlar:")
    print(f"   1. {exam1.title} ({exam1.get_exam_type_display()}) - {exam1.get_questions_count()} savol")
    print(f"   2. {exam2.title} ({exam2.get_exam_type_display()}) - {exam2.get_questions_count()} savol")
    print(f"   3. {exam3.title} ({exam3.get_exam_type_display()}) - {exam3.get_questions_count()} savol")
    print(f"\n📋 Ruxsatlar:")
    print(f"   teacher1 → barcha 3 imtihon tayinlangan")
    print(f"   IT-21 → Informatika oraliq + yakuniy")
    print(f"   IT-22 → Informatika oraliq")
    print(f"   MT-31 → hech narsa ko'ra olmaydi")
    print(f"\n🌐 Server: http://127.0.0.1:8000/")
    print(f"🔧 Admin panel: http://127.0.0.1:8000/admin/")


if __name__ == '__main__':
    create_test_data()
