# NextAI 2.0

نسخة تجريبية من NextAI بواجهة دردشة وربط Gemini.

## تشغيل مجاني بدون استضافة مدفوعة (Google Apps Script)

تم تجهيز نسخة خاصة بـ Apps Script داخل مجلد `apps-script`:

1. افتح https://script.google.com/home/start وأنشئ مشروعاً جديداً.
2. افتح `apps-script/Code.gs` من المستودع وانسخ محتواه إلى ملف `Code.gs` في المشروع.
3. أنشئ ملف HTML باسم `index` وانسخ إليه محتوى `apps-script/index.html`.
4. من **Project Settings → Script Properties** أضف:
   - Property: `GEMINI_API_KEY`
   - Value: مفتاح Gemini الخاص بك.
   - اختياري: `GEMINI_MODEL` = `gemini-2.5-flash`
5. اضغط **Deploy → New deployment → Web app**.
6. اختر **Execute as: Me**، وحدد صلاحية الوصول المناسبة لك، ثم **Deploy** وافتح رابط التطبيق.

لا تضع مفتاح Gemini داخل ملفات GitHub أو كود الواجهة. لا تشارك رابط التطبيق علناً إذا لم تكن تريد أن يستخدم الآخرون حصتك.

## حدود مهمة

Google Apps Script له حصص تشغيل يومية وحد أقصى لمدة التنفيذ؛ وGemini API له حصصه وحدوده الخاصة. راجع المصادر الرسمية قبل الاعتماد عليه استخداماً مكثفاً.

## النسخة الأصلية

الملفات `app.py` و`Dockerfile` تحفظ نسخة FastAPI للنشر على خادم يدعم Docker. لا تحتاجها لتشغيل نسخة Apps Script.
