# لوحة نشاط لayan

تحدّث GitHub Actions ملف `activity.json` كل 30 دقيقة من Trakt وChess.com وGitHub، وتقرأ بيانات الكتاب من `book.json`. السكربت يعمل على Node.js 18 أو أحدث ولا يحتاج إلى تثبيت حزم.

## الإعداد خطوة بخطوة

1. من إعدادات المستودع في GitHub، افتحي **Settings → Secrets and variables → Actions** ثم **New repository secret**. أضيفي السر باسم `TRAKT_CLIENT_ID` وضعي قيمة Client ID من إعدادات تطبيق Trakt.
2. راجعي أسماء الحسابات في `config.json`. اسم Trakt مضبوط على `layann`، والشطرنج على `laayyyaann`، وGitHub على `layan050`.
3. فعّلي GitHub Pages من **Settings → Pages**، واختاري النشر من فرع المستودع `main` ومجلد الجذر (`/root`). يحتاج القالب إلى أن يكون رابط JSON متاحاً على `https://layan050.github.io/life-dashboard/activity.json`.
4. شغّلي workflow المسمّى **Update activity** يدوياً من تبويب **Actions**. بعد نجاحه سيضيف أو يحدّث `activity.json` تلقائياً.
5. لتغيير الكتاب، عدّلي `enabled` و`name` و`progress` في `book.json` ثم شغّلي workflow يدوياً أو انتظري التشغيل المجدول. يمكن لاحقاً استبدال قارئ هذا الملف بمصدر مثل Goodreads RSS.

للتجربة محلياً: `node scripts/update-activity.mjs`. يلزم ضبط متغير البيئة `TRAKT_CLIENT_ID` كي يتحدث Trakt؛ عند تعذّر أي مصدر يحتفظ السكربت بآخر قيمته الناجحة في `activity.json` ويطبع تحذيراً.

## تحديث القالب

1. عدّلي `blogger-template.xml` مع الاحتفاظ بنسخة احتياطية في `templates/backup-YYYY-MM-DD.xml` قبل أي تعديل.
2. شغّلي `node scripts/validate-template.mjs` للتأكد من صحة XML وعناصر Blogger المطلوبة.
3. شغّلي `node scripts/copy-template.mjs` لنسخ القالب إلى الحافظة.
4. الصقيه في Blogger: **Theme** ثم السهم بجانب **Customize** ثم **Edit HTML** ثم **Ctrl+A** ثم **Ctrl+V** ثم **Save**.

> قالب Blogger غير موجود حالياً في نسخة المستودع هذه. أضيفي `blogger-template.xml` أولاً حتى تعمل أدوات التحقق والنسخ، وبعدها يمكن تطبيق تحديث البطاقة عليه.
