# 🎓 Test Platformasi - Student Test Management System

Bu loyiha studentlar uchun oraliq va yakuniy nazorat testlarini topshirish platformasidir. Django framework yordamida yaratilgan va PostgreSQL database ishlatiladi.

## 📋 Loyiha haqida

Test Platformasi - bu studentlarga online test topshirish, natijalarni ko'rish va o'qituvchilarga test yaratish imkoniyatini beruvchi to'liq funktsional web ilova.

### Asosiy imkoniyatlar:

- ✅ Foydalanuvchi tizimi (Student, O'qituvchi, Admin)
- ✅ Test yaratish va boshqarish
- ✅ Oraliq va yakuniy nazorat testlari
- ✅ Vaqt bilan cheklangan test topshirish
- ✅ Real-time taimer
- ✅ Avtomatik natija hisoblash
- ✅ Batafsil statistika
- ✅ Responsive dizayn
- ✅ PostgreSQL database

## 🏗️ Loyiha strukturasi

```
test_platform/
├── apps/                      # Barcha Django applar
│   ├── users/                # Foydalanuvchilar app
│   ├── exams/                # Imtihonlar app
│   ├── questions/            # Savollar app
│   └── results/              # Natijalar app
├── config/                    # Asosiy konfiguratsiya
│   ├── settings.py           # Django sozlamalari
│   ├── urls.py               # URL routing
│   ├── wsgi.py
│   └── asgi.py
├── templates/                 # HTML templatelar
│   ├── base.html
│   ├── users/
│   ├── exams/
│   └── results/
├── static/                    # Static fayllar (CSS, JS, images)
├── media/                     # Upload qilingan fayllar
├── manage.py
├── requirements.txt
└── README.md
```

## 🚀 O'rnatish va ishga tushirish

### 1. Talablar

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

### 2. PostgreSQL Database yaratish

```bash
# PostgreSQL ga kirish
psql -U postgres

# Database yaratish
CREATE DATABASE test_platform_db;

# Chiqish
\q
```

### 3. Virtual environment yaratish

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 4. Kerakli kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 5. Environment o'zgaruvchilari

`.env.example` faylidan `.env` yarating va o'zingizning ma'lumotlaringizni kiriting:

```bash
cp .env.example .env
```

`.env` faylida quyidagilarni o'zgartiring:
- `SECRET_KEY` - Django secret key
- `DB_PASSWORD` - PostgreSQL parol

### 6. Database migratsiyalarini ishga tushirish

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Superuser yaratish

```bash
python manage.py createsuperuser
```

### 8. Static fayllarni yig'ish

```bash
python manage.py collectstatic --noinput
```

### 9. Serverni ishga tushirish

```bash
python manage.py runserver
```

Endi brauzeringizda `http://127.0.0.1:8000/` manzilini oching!

## 👥 Foydalanuvchi turlari

### 1. Student
- Testlarni topshirish
- Natijalarni ko'rish
- Profil boshqarish

### 2. O'qituvchi
- Test yaratish
- Savollar qo'shish
- Studentlar natijalarini ko'rish

### 3. Admin
- Barcha tizim boshqaruvi
- Foydalanuvchilar boshqaruvi
- Statistika

## 🎯 Asosiy sahifalar

- `/` - Dashboard
- `/login/` - Tizimga kirish
- `/register/` - Ro'yxatdan o'tish
- `/exams/` - Imtihonlar ro'yxati
- `/exams/<id>/` - Imtihon tafsilotlari
- `/exams/<id>/take/` - Test topshirish
- `/results/` - Natijalar
- `/admin/` - Admin panel

## 📱 Ekran ko'rinishlari

### Asosiy funksiyalar:

1. **Login/Register** - Foydalanuvchi tizimi
2. **Dashboard** - Asosiy sahifa
3. **Imtihonlar ro'yxati** - Barcha mavjud testlar
4. **Test topshirish** - Real-time timer bilan
5. **Natijalar** - Batafsil statistika

## 🔧 Admin panel

Admin panelga kirish uchun:
1. `http://127.0.0.1:8000/admin/` ga o'ting
2. Superuser login va parolini kiriting
3. Bu yerdan siz:
   - Fanlar qo'shishingiz
   - Imtihonlar yaratishingiz
   - Savollar va javoblar qo'shishingiz
   - Natijalarni ko'rishingiz mumkin

## 📊 Database modellari

### CustomUser
- Foydalanuvchi ma'lumotlari
- User type (student, teacher, admin)
- Guruh, kurs

### Subject
- Fan nomi va tavsifi

### Exam
- Imtihon nomi
- Fan
- Imtihon turi (oraliq, yakuniy, mashq)
- Vaqt, ball sozlamalari

### Question
- Savol matni
- Rasm (optional)
- Qiyinlik darajasi
- Ball

### Answer
- Javob matni
- To'g'ri/noto'g'ri
- Savol bilan bog'lanish

### ExamAttempt
- Studentning imtihon urinishi
- Status (jarayonda, yakunlangan)

### ExamResult
- Imtihon natijasi
- Ball, foiz, baho
- To'g'ri/noto'g'ri javoblar

## 🔐 Xavfsizlik

- CSRF himoyasi
- Password hashing
- Login required decorators
- User permissions

## 🌐 Texnologiyalar

- **Backend:** Django 4.2
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript
- **Styling:** Custom CSS (Gradient design)
- **Icons:** Unicode emojis

## 📝 Imtihon yaratish qo'llanmasi

1. Admin panelga kiring
2. **Subjects** bo'limidan fan qo'shing
3. **Exams** bo'limidan imtihon yarating:
   - Nom, fan, tur
   - Vaqt, ball sozlamalari
   - Guruhlar (optional)
4. **Questions** bo'limidan savollar qo'shing:
   - Har bir savol uchun 4 ta javob
   - To'g'ri javobni belgilang

## 🐛 Xato va muammolar

Agar muammo yuzaga kelsa:

1. Virtual environment faol ekanligini tekshiring
2. Database sozlamalari to'g'ri ekanligini tekshiring
3. Migrations ishga tushganligini tekshiring
4. Log fayllarni tekshiring

## 📞 Yordam

Savol va takliflar uchun:
- GitHub Issues
- Email: [sizning@email.uz]

## 📄 Litsenziya

MIT License

## 🎉 Hissa qo'shish

Pull request'lar xush kelibsiz! Katta o'zgarishlar uchun avval issue oching.

---

**Muvaffaqiyatlar!** 🚀
