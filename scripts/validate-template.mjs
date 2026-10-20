import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const fail = (message) => { console.error(`فشل التحقق: ${message}`); process.exitCode = 1; };
let xml;
try { xml = await readFile(path.join(root, 'blogger-template.xml'), 'utf8'); }
catch { fail('الملف blogger-template.xml غير موجود في جذر المستودع.'); process.exit(); }

function checkWellFormed(source) {
  const tokens = source.match(/<!--[\s\S]*?-->|<\?[\s\S]*?\?>|<!\[CDATA\[[\s\S]*?\]\]>|<!DOCTYPE(?:\s[^>]*)?>|<[^>]+>|[^<]+/g) ?? [];
  if (tokens.join('') !== source) throw new Error('تعذر تحليل بعض علامات XML.');
  const stack = [];
  for (const token of tokens) {
    if (token.startsWith('<!--')) { if (token.slice(4, -3).includes('--')) throw new Error('تعليق XML غير صالح.'); continue; }
    if (token.startsWith('<?') || token.startsWith('<!DOCTYPE') || token.startsWith('<![CDATA[')) continue;
    if (token.startsWith('</')) {
      const name = token.match(/^<\/([\w:.-]+)\s*>$/)?.[1];
      if (!name || stack.pop() !== name) throw new Error(`وسم إغلاق غير متطابق: ${token}`);
    } else if (token.startsWith('<')) {
      const match = token.match(/^<([\w:.-]+)(?:\s[^<>]*?)?\s*(\/?)>$/s);
      if (!match) throw new Error(`وسم XML غير صالح: ${token.slice(0, 80)}`);
      const [, name, selfClosing] = match;
      const attrs = token.slice(name.length + 1, selfClosing ? -2 : -1);
      const attrPattern = /([\w:.-]+)\s*=\s*("[^"]*"|'[^']*')/gy;
      let position = 0;
      while (position < attrs.length) {
        while (/\s/.test(attrs[position] ?? '') || attrs[position] === '/') position++;
        if (position >= attrs.length) break;
        attrPattern.lastIndex = position;
        const attr = attrPattern.exec(attrs);
        if (!attr) throw new Error(`خاصية غير صالحة في <${name}>.`);
        if (attr[2].slice(1, -1).includes('<')) throw new Error(`محرف < في خاصية <${name}>.`);
        position = attrPattern.lastIndex;
      }
      if (!selfClosing) stack.push(name);
    } else if (token.includes(']]>')) throw new Error('إغلاق CDATA غير مطابق.');
  }
  if (stack.length) throw new Error(`وسم غير مغلق: <${stack.at(-1)}>.`);
  if ((source.match(/<!\[CDATA\[/g) ?? []).length !== (source.match(/\]\]>/g) ?? []).length) throw new Error('كتل CDATA غير متوازنة.');
}

try { checkWellFormed(xml); } catch (error) { fail(`XML غير صالح: ${error.message}`); }
if (!/<b:skin(?:\s|>)/.test(xml)) fail('عنصر b:skin غير موجود.');
if (!/<b:section(?:\s|>)/.test(xml)) fail('عنصر b:section غير موجود.');
if (!/<b:widget\b(?=[^>]*\bid\s*=\s*(['"])Blog1\1)[^>]*>/.test(xml)) fail('عنصر b:widget بالمعرّف Blog1 غير موجود.');
if (xml.includes('MANUAL_CONFIG')) fail('القالب ما زال يحتوي MANUAL_CONFIG.');
if (/https?:\/\/api\.(?:chess\.com|github\.com)\//i.test(xml)) fail('القالب ما زال يطلب Chess.com أو GitHub مباشرة.');
if (!process.exitCode) console.log('نجاح: القالب XML سليم ويحتوي عناصر Blogger المطلوبة.');
