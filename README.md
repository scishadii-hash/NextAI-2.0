---
title: NextAI 2.0
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# NextAI 2.0

مساعد دردشة تجريبي يعمل باستخدام FastAPI وGemini.

## تشغيله على Hugging Face Spaces

1. أنشئ Space جديداً واختر **Docker**.
2. اربط مستودع GitHub هذا: https://github.com/scishadii-hash/NextAI-2.0
3. من **Settings → Variables and secrets** أضف Secret باسم `GEMINI_API_KEY` وضع قيمة مفتاح Gemini.
4. انتظر اكتمال البناء وافتح التطبيق.

## إعدادات اختيارية

- `GEMINI_MODEL`: اسم النموذج. الافتراضي `gemini-2.5-flash`.
- المنفذ مضبوط على `7860` ليتوافق مع Hugging Face Spaces.

## محلياً

```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your-key"
uvicorn app:app --reload
```

لا تضع مفتاح API داخل ملفات المستودع أو في الواجهة. استخدام Gemini API قد يخضع لحصص وحدود مجانية أو رسوم حسب حساب Google AI Studio.
