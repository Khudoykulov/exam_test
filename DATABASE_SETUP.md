# Database O'rnatish Qo'llanmasi

## PostgreSQL o'rnatish

### Windows uchun:
1. PostgreSQL rasmiy saytidan yuklab oling: https://www.postgresql.org/download/windows/
2. Installer'ni ishga tushiring va ko'rsatmalarga rioya qiling
3. Parol o'rnating va eslab qoling

### Linux (Ubuntu/Debian) uchun:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### macOS uchun:
```bash
brew install postgresql
brew services start postgresql
```

## Database yaratish

### 1. PostgreSQL ga kirish:

**Windows:**
```bash
psql -U postgres
```

**Linux:**
```bash
sudo -u postgres psql
```

### 2. Database va user yaratish:

```sql
-- Database yaratish
CREATE DATABASE test_platform_db;

-- User yaratish (optional)
CREATE USER test_platform_user WITH PASSWORD 'your_password';

-- User'ga ruxsatlar berish
ALTER ROLE test_platform_user SET client_encoding TO 'utf8';
ALTER ROLE test_platform_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE test_platform_user SET timezone TO 'Asia/Tashkent';
GRANT ALL PRIVILEGES ON DATABASE test_platform_db TO test_platform_user;

-- Chiqish
\q
```

### 3. Database connection test:

```bash
psql -U postgres -d test_platform_db -c "SELECT version();"
```

## Django bilan ulanish

`config/settings.py` faylida database sozlamalari:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_platform_db',
        'USER': 'postgres',  # yoki test_platform_user
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Migrations

```bash
# Migratsiya fayllarini yaratish
python manage.py makemigrations

# Migratsiyalarni ishga tushirish
python manage.py migrate

# Migratsiyalarni ko'rish
python manage.py showmigrations
```

## Test data yaratish

### 1. Superuser:
```bash
python manage.py createsuperuser
```

### 2. Admin panel orqali:
- http://127.0.0.1:8000/admin/ ga kiring
- Subject yarating
- Exam yarating
- Question va Answer qo'shing

### 3. Django shell orqali:

```bash
python manage.py shell
```

```python
from apps.users.models import CustomUser
from apps.exams.models import Subject, Exam
from apps.questions.models import Question, Answer
from django.utils import timezone
from datetime import timedelta

# Subject yaratish
subject = Subject.objects.create(
    name="Matematika",
    description="Oliy matematika kursi"
)

# Teacher yaratish
teacher = CustomUser.objects.create_user(
    username='teacher1',
    email='teacher@example.com',
    password='password123',
    first_name='Alisher',
    last_name='Navoiy',
    user_type='teacher'
)

# Exam yaratish
exam = Exam.objects.create(
    title="Matematika Oraliq Nazorat 1",
    subject=subject,
    exam_type='midterm',
    description="Birinchi oraliq nazorat testi",
    duration=60,
    total_marks=100,
    passing_marks=60,
    start_time=timezone.now(),
    end_time=timezone.now() + timedelta(days=7),
    is_active=True,
    created_by=teacher,
    allowed_groups="IT-21,IT-22"
)

# Savol yaratish
question1 = Question.objects.create(
    exam=exam,
    question_text="2 + 2 nechaga teng?",
    difficulty='easy',
    marks=10,
    order=1
)

# Javoblar yaratish
Answer.objects.create(question=question1, answer_text="3", is_correct=False, order=1)
Answer.objects.create(question=question1, answer_text="4", is_correct=True, order=2)
Answer.objects.create(question=question1, answer_text="5", is_correct=False, order=3)
Answer.objects.create(question=question1, answer_text="6", is_correct=False, order=4)

print("Test data muvaffaqiyatli yaratildi!")
```

## Database backup

```bash
# Backup yaratish
pg_dump -U postgres test_platform_db > backup.sql

# Backup'dan qayta tiklash
psql -U postgres test_platform_db < backup.sql
```

## Muammolarni hal qilish

### Muammo 1: "FATAL: role does not exist"
```bash
# User yaratish
createuser -U postgres test_platform_user
```

### Muammo 2: "FATAL: database does not exist"
```bash
# Database yaratish
createdb -U postgres test_platform_db
```

### Muammo 3: Permission denied
```bash
# Linux uchun
sudo -u postgres psql
```

### Muammo 4: Connection refused
```bash
# PostgreSQL service'ni ishga tushirish
# Windows
net start postgresql-x64-14
# Linux
sudo systemctl start postgresql
```
