import { readFile } from 'node:fs/promises';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import os from 'node:os';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const xml = await readFile(path.join(root, 'blogger-template.xml'), 'utf8');
const platform = os.platform();
const command = platform === 'darwin' ? 'pbcopy' : platform === 'win32' ? 'clip' : 'xclip';
const args = platform === 'linux' ? ['-selection', 'clipboard'] : [];
await new Promise((resolve, reject) => {
  const child = spawn(command, args, { stdio: ['pipe', 'ignore', 'pipe'] });
  let errorOutput = '';
  child.stderr.setEncoding('utf8').on('data', chunk => errorOutput += chunk);
  child.on('error', error => reject(new Error(`تعذر تشغيل ${command}: ${error.message}`)));
  child.on('close', code => code === 0 ? resolve() : reject(new Error(`فشل ${command} (${code}): ${errorOutput}`)));
  child.stdin.end(xml);
});
console.log('تم نسخ القالب إلى الحافظة.');
console.log('في Blogger: Theme ثم السهم بجانب Customize ثم Edit HTML ثم Ctrl+A ثم Ctrl+V ثم Save.');
