# 🚀 Test Platformasi O'rnatish Qo'llanmasi

## Tizim talablari

- Python 3.8 yoki yuqoriroq versiya
- PostgreSQL 12 yoki yuqoriroq versiya
- pip (Python package manager)
- Git (optional, loyihani yuklab olish uchun)

## Qadam-baqadam o'rnatish

### 1. Loyihani yuklab olish

```bash
# Agar GitHub'da bo'lsa
git clone [repository-url]
cd test_platform

# Yoki ZIP faylini yuklab olib, ochib oling
```

### 2. Virtual environment yaratish va faollashtirish

**Windows uchun:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS uchun:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Virtual environment faollashganda terminal'da `(venv)` ko'rinadi.

### 3. Kerakli kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

Bu jarayon bir necha daqiqa davom etishi mumkin.

### 4. PostgreSQL o'rnatish va sozlash

#### Windows:
1. https://www.postgresql.org/download/windows/ dan PostgreSQL yuklab oling
2. Installer'ni ishga tushiring
3. Parol o'rnating va eslab qoling (masalan: `postgres123`)
4. Port: `5432` (default)

#### Linux (Ubuntu):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### macOS:
```bash
brew install postgresql
brew services start postgresql
```

### 5. Database yaratish

PostgreSQL ga kirish:

**Windows:**
```bash
psql -U postgres
```

**Linux:**
```bash
sudo -u postgres psql
```

Database yaratish (PostgreSQL shell'da):
```sql
CREATE DATABASE test_platform_db;
\q
```

### 6. Environment faylini sozlash

`.env.example` faylidan `.env` yarating:

**Windows:**
```bash
copy .env.example .env
```

**Linux/macOS:**
```bash
cp .env.example .env
```

`.env` faylini ochib, quyidagi qatorlarni o'zgartiring:
```
SECRET_KEY=your-random-secret-key-here-change-this
DB_PASSWORD=postgres123  # PostgreSQL'da o'rnatgan parolingiz
```

### 7. Database migratsiyalarini ishga tushirish

```bash
python manage.py makemigrations
python manage.py migrate
```

Bu buyruqlar database strukturasini yaratadi.

### 8. Superuser (Admin) yaratish

```bash
python manage.py createsuperuser
```

Sizdan so'raladi:
- Username: `admin` (yoki o'zingiz xohlagan)
- Email: `admin@example.com`
- Password: `admin123` (yoki o'zingiz xohlagan)
- Password confirmation: Parolni takrorlang

### 9. Static fayllarni yig'ish

```bash
python manage.py collectstatic --noinput
```

### 10. Serverni ishga tushirish

```bash
python manage.py runserver
```

Brauzeringizda quyidagi manzilni oching:
```
http://127.0.0.1:8000/
```

## ✅ Tekshirish

1. **Admin panel:** http://127.0.0.1:8000/admin/
   - Superuser login va parol bilan kiring
   
2. **Asosiy sahifa:** http://127.0.0.1:8000/
   - Login sahifasi ochilishi kerak

## 📝 Test ma'lumotlarini kiritish

### Admin panel orqali (Tavsiya etiladi):

1. http://127.0.0.1:8000/admin/ ga kiring
2. **Subjects** bo'limida fanlari qo'shing:
   - Name: Matematika
   - Description: Oliy matematika kursi
   
3. **Custom users** bo'limida student yarating:
   - Username: student1
   - Password: student123
   - User type: Student
   - Group: IT-21
   
4. **Exams** bo'limida imtihon yarating:
   - Title: Matematika Oraliq Nazorat
   - Subject: Matematika
   - Exam type: Midterm
   - Duration: 60 (daqiqa)
   - Total marks: 100
   - Passing marks: 60
   - Start time: Hozirgi vaqt
   - End time: Bir hafta keyin
   - Created by: admin (superuser)
   
5. **Questions** bo'limida savol qo'shing:
   - Exam: tanlang
   - Question text: "2 + 2 nechaga teng?"
   - Difficulty: Easy
   - Marks: 10
   - Order: 1
   - Save qiling
   
6. Savolning sahifasida **Answers** bo'limida 4 ta javob qo'shing:
   - Answer 1: "3" (is_correct: unchecked)
   - Answer 2: "4" (is_correct: CHECKED) ✓
   - Answer 3: "5" (is_correct: unchecked)
   - Answer 4: "6" (is_correct: unchecked)

### Test qilish:

1. Logout qiling
2. `student1` / `student123` bilan login qiling
3. Imtihonlar ro'yxatini ko'ring
4. Imtihonni boshlang va topshiring
5. Natijalarni ko'ring

## 🐛 Muammolarni hal qilish

### Muammo 1: "ModuleNotFoundError: No module named 'django'"
**Yechim:**
```bash
# Virtual environment faolligini tekshiring
# Agar yo'q bo'lsa:
pip install -r requirements.txt
```

### Muammo 2: "django.db.utils.OperationalError: FATAL: database does not exist"
**Yechim:**
```bash
# PostgreSQL ga kiring va database yarating
psql -U postgres
CREATE DATABASE test_platform_db;
\q
```

### Muammo 3: "django.db.utils.OperationalError: FATAL: password authentication failed"
**Yechim:**
- `.env` faylidagi `DB_PASSWORD` to'g'ri ekanligini tekshiring
- PostgreSQL parolini to'g'ri kiriting

### Muammo 4: Port 8000 band
**Yechim:**
```bash
# Boshqa portda ishga tushiring
python manage.py runserver 8001
```

### Muammo 5: Static fayllar yuklanmayapti
**Yechim:**
```bash
python manage.py collectstatic --noinput
# Keyin serverni qayta ishga tushiring
```

## 📱 Keyingi qadamlar

1. **Fanlari qo'shing:** Admin panelda Subject yarating
2. **Imtihonlar yarating:** Exam modelida yangi testlar qo'shing
3. **Savollar qo'shing:** Har bir imtihon uchun Question va Answer yarating
4. **Studentlar qo'shing:** Yangi foydalanuvchilar yarating
5. **Test qiling:** Student sifatida imtihon topshiring

## 🆘 Yordam

Agar muammo hal bo'lmasa:
1. Terminal'dagi xato xabarini diqqat bilan o'qing
2. `python manage.py check` buyrug'ini ishga tushiring
3. Log fayllarni tekshiring

## 🎉 Tayyor!

Endi siz test platformasi bilan ishlashingiz mumkin! 

Muaffaqiyatlar! 🚀
