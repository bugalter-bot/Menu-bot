# 🍽 Shaxsiy Taomlar Menu Bot

Telegram bot: taomlaringizni bo'lim (quyuq/suyuq/hamirli va o'zingiz qo'shgan bo'limlar) bo'yicha saqlaysiz, ko'rasiz, qidirasiz va ikkilanganingizda **Random** tugmasi orqali taom tanlab beradi.

## Imkoniyatlar
- 📂 Bo'limlar: standart (Quyuq, Suyuq, Hamirli) + o'zingiz xohlagancha qo'shing
- ➕ Har bir bo'limga taom qo'shish: nomi, rasmi (ixtiyoriy), retsepti (ixtiyoriy)
- 📋 Hammasi — barcha taomlarni bitta ro'yxatda ko'rish
- 🔍 Qidirish — taom nomi bo'yicha qidirish
- 🎲 Random — barcha taomlardan yoki tanlangan bo'limdan random taom tanlash
- ✏️ Tahrirlash / 🗑 O'chirish — har bir taom va bo'lim uchun
- 📦 Backup — barcha taomlarni JSON fayl qilib olish
- 🔒 Faqat sizning Telegram ID'ingiz bilan ishlaydi (ADMIN_ID)

## 1. Bot yaratish
1. Telegram'da [@BotFather](https://t.me/BotFather) ga `/newbot` yozing, nomini bering.
2. Sizga beriladigan **tokenni** saqlab qo'ying.
3. O'z Telegram ID'ingizni bilish uchun [@userinfobot](https://t.me/userinfobot) ga `/start` yozing.

## 2. Ma'lumotlar bazasi (Neon)
1. [neon.tech](https://neon.tech) da ro'yxatdan o'ting, yangi loyiha yarating.
2. Dashboard'dan **Connection string** (Pooled connection) ni nusxalang — bu `DATABASE_URL` bo'ladi.

## 3. GitHub'ga yuklash
```bash
cd telegram-menu-bot
git init
git add .
git commit -m "Menu bot"
git branch -M main
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```
> `.env` fayli hech qachon yuklanmaydi (`.gitignore` da bor).

## 4. Render'da deploy qilish
1. [render.com](https://render.com) → **New +** → **Web Service** → GitHub repongizni tanlang.
2. Sozlamalar:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `python main.py`
3. **Environment** bo'limida quyidagilarni qo'shing:
   - `BOT_TOKEN` — BotFather'dan olingan token
   - `DATABASE_URL` — Neon'dan olingan connection string
   - `ADMIN_ID` — sizning Telegram ID'ingiz
   - `WEBHOOK_HOST` — deploy tugagach Render bergan URL (masalan `https://telegram-menu-bot.onrender.com`) — birinchi deploydan keyin qo'shib, qayta deploy qiling
4. Deploy tugagach, bot avtomatik webhook o'rnatadi va ishga tushadi.

## 5. UptimeRobot bilan doim tirik saqlash
1. [uptimerobot.com](https://uptimerobot.com) da monitor yarating.
2. **Monitor Type:** HTTP(s)
3. **URL:** `https://<your-app>.onrender.com/health`
4. **Interval:** 5 daqiqa

Bu Render'ning bepul rejasida bot "uxlab qolishi"ning oldini oladi.

## Lokal test qilish
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # va qiymatlarni to'ldiring
python main.py
```
Lokalda ishga tushirsangiz `WEBHOOK_HOST`ni bo'sh qoldiring — shunda webhook o'rnatilmaydi (kerak bo'lsa keyinchalik polling rejimiga o'tkazish mumkin).

## Loyiha tuzilishi
```
telegram-menu-bot/
├── main.py            # webhook server + botni ishga tushirish
├── config.py          # environment o'zgaruvchilar
├── database.py        # Neon Postgres bilan ishlash
├── keyboards.py        # inline tugmalar
├── states.py           # FSM holatlari
├── middleware.py        # faqat admin uchun ruxsat
└── handlers/
    ├── common.py       # /start, bosh menu
    ├── categories.py   # bo'limlar
    ├── foods.py        # taomlar (qo'shish/ko'rish/tahrirlash/o'chirish)
    ├── random_pick.py  # 🎲 random
    ├── search.py       # 🔍 qidirish
    └── backup.py       # 📦 backup
```
