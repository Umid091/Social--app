# 📱 Social App — Django REST API

> Instagram'ga o'xshash ijtimoiy tarmoq uchun REST API backend. JWT autentifikatsiya, ko'p bosqichli ro'yxatdan o'tish, postlar, storylar, izohlar, like va follow tizimi mavjud.

---

## 📋 Mundarija

- [Loyiha haqida](#loyiha-haqida)
- [Imkoniyatlar](#imkoniyatlar)
- [Texnologiyalar](#texnologiyalar)
- [Loyiha tuzilmasi](#loyiha-tuzilmasi)
- [Ishga tushirish](#ishga-tushirish)
- [Muhit o'zgaruvchilari](#muhit-ozgaruvchilari)
- [API endpointlari](#api-endpointlari)
- [Ma'lumotlar modeli](#malumotlar-modeli)
- [Autentifikatsiya jarayoni](#autentifikatsiya-jarayoni)

---

## 📌 Loyiha haqida

**Social App** — Django va Django REST Framework asosida qurilgan to'liq funksional ijtimoiy tarmoq backend API'si. Foydalanuvchilar email yoki telefon raqami orqali ro'yxatdan o'tishi, tasdiqlash kodi bilan o'z shaxsini tasdiqlashi, postlar va storylar joylash, like va izoh qoldirish, hamda boshqa foydalanuvchilarga obuna bo'lishi mumkin.

Bu loyiha real dunyodagi backend muhandislik amaliyotlarini — maxsus autentifikatsiya, token blacklisting, ko'p bosqichli ro'yxatdan o'tish va media fayllarni boshqarishni o'rganish maqsadida yaratilgan.

---

## ✨ Imkoniyatlar

### 🔐 Autentifikatsiya va foydalanuvchi boshqaruvi
- **Ko'p bosqichli ro'yxatdan o'tish** — email yoki telefon → tasdiqlash kodi → profil ma'lumotlari → rasm yuklash
- **JWT autentifikatsiya** — `djangorestframework-simplejwt` orqali access va refresh tokenlar
- **Token Blacklisting** — logout paytida refresh token bekor qilinadi
- **Token yangilash** — refresh token orqali yangi access token olish
- **Moslashuvchan login** — **username**, **email** yoki **telefon raqam** bilan kirish
- **Parolni tiklash** — email yoki telefonga tasdiqlash kodi yuboriladi
- **Parolni yangilash** — tasdiqlashdan so'ng yangi parol o'rnatish

### 👤 Foydalanuvchi profili
- `AbstractUser` kengaytirgan maxsus foydalanuvchi modeli
- Rollar: `ordinary_user`, `admin`, `manager`
- Auth holat kuzatuvi: `new` → `code_verify` → `done` → `photo_done`
- Bio va avatar rasm bilan profil
- Yangi foydalanuvchilar uchun avtomatik unikal username generatsiyasi
- UUID asosidagi primary keylar

### 📸 Kontent
- **Postlar** — caption bilan rasm postlar
- **Storylar** — 24 soatdan keyin avtomatik o'chuvchi rasm/video storylar
- **Izohlar** — postlarga joylashtirilgan (nested) izohlar
- **Story izohlari** — storylarga izohlar

### ❤️ Interaksiyalar
- **Post likelari** — postni like/unlike qilish (har bir foydalanuvchi uchun 1 ta)
- **Izoh likelari** — izohlarga like/unlike (har bir foydalanuvchi uchun 1 ta)
- **Story likelari** — storylarga like/unlike (har bir foydalanuvchi uchun 1 ta)
- **Follow tizimi** — foydalanuvchilarga obuna/obunadan chiqish (unikal juftlik)

---

## 🛠 Texnologiyalar

| Texnologiya | Versiya | Maqsad |
|---|---|---|
| Python | 3.x | Dasturlash tili |
| Django | 6.0.2 | Web framework |
| Django REST Framework | so'nggi | REST API toolkit |
| djangorestframework-simplejwt | so'nggi | JWT autentifikatsiya |
| SQLite | ichki | Development bazasi |
| Gmail SMTP | — | Email tasdiqlash |

---

## 🗂 Loyiha tuzilmasi

```
cosial_app/
├── config/                  # Django loyiha konfiguratsiyasi
│   ├── settings.py          # Sozlamalar (JWT, email, baza va h.k.)
│   ├── urls.py              # Root URL konfiguratsiyasi
│   ├── asgi.py
│   └── wsgi.py
│
├── users/                   # Autentifikatsiya va foydalanuvchi app
│   ├── models.py            # CustomUser, CodeVerify modellari
│   ├── serializers.py       # SignUp, Login, Password, Photo serializerlari
│   ├── views.py             # Auth view'lar (register, login, logout va h.k.)
│   ├── urls.py              # Auth URL pattern'lar
│   └── admin.py
│
├── posts/                   # Ijtimoiy kontent app
│   ├── models.py            # Post, Profile, Comment, Like, Follow, Story modellari
│   ├── views.py
│   └── admin.py
│
├── shared/                  # Umumiy yordamchi modullar
│   ├── models.py            # BaseModel (UUID PK, timestamplar)
│   └── utility.py           # Email/telefon validatorlar, send_email yordamchisi
│
├── media/                   # Foydalanuvchi yuklagan fayllar (gitignore'da)
├── manage.py
└── db.sqlite3
```

---

## 🚀 Ishga tushirish

### Talablar
- Python 3.8+
- pip

### 1. Repozitoriyani clone qiling
```bash
git clone https://github.com/Umid091/Social--app.git
cd Social--app
```

### 2. Virtual muhit yarating va faollashtiring
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Kutubxonalarni o'rnating
```bash
pip install django djangorestframework djangorestframework-simplejwt pillow
```

### 4. Muhit o'zgaruvchilarini sozlang
`config/settings.py` faylida quyidagi qiymatlarni yangilang (pastga qarang):
- `SECRET_KEY`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`

### 5. Migratsiyalarni bajaring
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Superuser yarating (ixtiyoriy)
```bash
python manage.py createsuperuser
```

### 7. Development serverni ishga tushiring
```bash
python manage.py runserver
```

API manzili: `http://127.0.0.1:8000/`

---

## ⚙️ Muhit o'zgaruvchilari

Quyidagi sozlamalar `config/settings.py` da joylashgan. Production uchun ularni `.env` fayliga yoki environment variable'larga ko'chiring:

| O'zgaruvchi | Tavsif | Standart |
|---|---|---|
| `SECRET_KEY` | Django maxfiy kaliti | dev uchun xavfsiz emas |
| `DEBUG` | Debug rejim | `True` |
| `EMAIL_HOST_USER` | Kod yuboruvchi Gmail manzil | — |
| `EMAIL_HOST_PASSWORD` | Gmail App Parol | — |
| `EMAIL_EXPIRATION_TIME` | Email kod muddati (daqiqa) | `3` |
| `PHONE_EXPIATION_TIME` | Telefon kod muddati (daqiqa) | `2` |

> ⚠️ **Diqqat:** Haqiqiy maxfiy kalitlar yoki email parollarni version control'ga commit qilmang. Production'da environment variable'lardan foydalaning.

---

## 🔗 API Endpointlari

### Autentifikatsiya — `/auth/`

| Metod | Endpoint | Auth kerakmi | Tavsif |
|---|---|---|---|
| `POST` | `/auth/sign-up/` | ❌ | Email yoki telefon bilan ro'yxatdan o'tish |
| `POST` | `/auth/code_verify/` | ✅ | Tasdiqlash kodini kiritish |
| `GET` | `/auth/get-new-code/` | ✅ | Yangi tasdiqlash kodi so'rash |
| `PUT` | `/auth/user-update/` | ✅ | Profilni to'ldirish (ism, username, parol) |
| `PATCH` | `/auth/photo-update/` | ✅ | Profil rasmini yuklash |
| `POST` | `/auth/login/` | ❌ | Tizimga kirish (username / email / telefon) |
| `POST` | `/auth/logout/` | ✅ | Tizimdan chiqish (refresh token bekor qilinadi) |
| `GET` | `/auth/login-refresh/` | ❌ | Access tokenni yangilash |
| `POST` | `/auth/forgot-password/` | ❌ | Parolni tiklash kodi so'rash |
| `PATCH` | `/auth/reset-password/` | ✅ | Yangi parol o'rnatish |

### Misol: Yangi foydalanuvchi ro'yxatdan o'tishi

**So'rov:**
```http
POST /auth/sign-up/
Content-Type: application/json

{
    "email_or_phone": "foydalanuvchi@example.com"
}
```

**Javob:**
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "auth_status": "new",
    "auth_type": "via_email",
    "message": "Kodingiz yuborildi",
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}
```

### Misol: Tizimga kirish

**So'rov:**
```http
POST /auth/login/
Content-Type: application/json

{
    "user_input": "john_doe",
    "password": "parol12345"
}
```

**Javob:**
```json
{
    "message": "login bajarildi",
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}
```

---

## 🗃 Ma'lumotlar modeli

### CustomUser
| Maydon | Tur | Tavsif |
|---|---|---|
| `id` | UUID | Birlamchi kalit (avtomatik) |
| `username` | string | Unikal username (bo'sh bo'lsa avtomatik yaratiladi) |
| `email` | string | Unikal email manzil |
| `phone_number` | string | Unikal telefon raqam (`+998XXXXXXXXX`) |
| `photo` | rasm | Profil rasmi (jpg, jpeg, png) |
| `user_role` | tanlov | `ordinary_user` / `admin` / `manager` |
| `auth_status` | tanlov | `new` → `code_verify` → `done` → `photo_done` |
| `auth_type` | tanlov | `via_email` / `via_phone` |
| `created_at` | datetime | Yaratilgan vaqt |
| `update_at` | datetime | Oxirgi yangilanish vaqti |

### Post
| Maydon | Tur | Tavsif |
|---|---|---|
| `id` | int | Birlamchi kalit |
| `user` | FK → CustomUser | Post muallifi |
| `image` | rasm | Post rasmi (majburiy) |
| `caption` | matn | Ixtiyoriy izoh |
| `create_at` | datetime | Yaratilgan vaqt |

### Story
| Maydon | Tur | Tavsif |
|---|---|---|
| `id` | int | Birlamchi kalit |
| `user` | FK → CustomUser | Story muallifi |
| `image` | rasm | Ixtiyoriy rasm |
| `video` | fayl | Ixtiyoriy video |
| `text` | string | Ixtiyoriy matn (max 500 belgi) |
| `expires_at` | datetime | Yaratilgandan 24 soat o'tgach o'chadi |
| `created_at` | datetime | Yaratilgan vaqt |

### Comment
| Maydon | Tur | Tavsif |
|---|---|---|
| `id` | int | Birlamchi kalit |
| `post` | FK → Post | Tegishli post |
| `user` | FK → CustomUser | Izoh muallifi |
| `parent` | FK → o'ziga | Ota izoh (ichki javoblar uchun) |
| `text` | matn | Izoh matni |
| `created_at` | datetime | Yaratilgan vaqt |

### Follow
| Maydon | Tur | Tavsif |
|---|---|---|
| `follower` | FK → CustomUser | Obuna bo'luvchi foydalanuvchi |
| `following` | FK → CustomUser | Obuna bo'linayotgan foydalanuvchi |
| `created_at` | datetime | Obuna vaqti |

> `unique_together` cheklovi bir xil juftlikning qayta yaratilishiga yo'l qo'ymaydi.

---

## 🔑 Autentifikatsiya jarayoni

```
1. POST /auth/sign-up/
   └─ Kirish: email yoki telefon raqam
   └─ Chiqish: access + refresh tokenlar, tasdiqlash kodi yuboriladi

2. POST /auth/code_verify/
   └─ Kirish: tasdiqlash kodi (Bearer token talab etiladi)
   └─ Chiqish: yangilangan tokenlar, auth_status → "code_verify"

3. PUT /auth/user-update/
   └─ Kirish: ism, familiya, username, parol, parolni tasdiqlash
   └─ Chiqish: yangilangan tokenlar, auth_status → "done"

4. PATCH /auth/photo-update/  (ixtiyoriy)
   └─ Kirish: profil rasmi
   └─ Chiqish: yangilangan tokenlar, auth_status → "photo_done"

5. POST /auth/login/           (qaytgan foydalanuvchilar uchun)
   └─ Kirish: user_input (username/email/telefon) + parol
   └─ Chiqish: access + refresh tokenlar
```

---

## 👨‍💻 Muallif

**Umid Jorayev**
- GitHub: [@Umid091](https://github.com/Umid091)

---

## 📄 Litsenziya

Ushbu loyiha ochiq manbali va [MIT Litsenziyasi](LICENSE) ostida tarqatiladi.
