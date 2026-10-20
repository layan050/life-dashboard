import { readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const readJson = async (file, fallback) => {
  try { return JSON.parse(await readFile(path.join(root, file), 'utf8')); }
  catch (error) { if (error.code === 'ENOENT') return fallback; throw error; }
};
const config = await readJson('config.json', {});
const previous = await readJson('activity.json', {});
const labels = { book: 'الكتاب', show: 'المسلسل' };
const warning = (source, error) => console.warn(`تحذير: تعذّر تحديث ${source}؛ سنحتفظ بآخر قيمة صحيحة. ${error.message}`);
async function request(url, options = {}) {
  const response = await fetch(url, { signal: AbortSignal.timeout(15000), ...options });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

let book = { enabled: false, label: labels.book, ...(previous.book ?? {}) };
try {
  const manual = await readJson('book.json', {});
  if (typeof manual.enabled === 'boolean' && manual.name?.trim() && manual.progress?.trim()) {
    book = { enabled: manual.enabled, label: labels.book, name: manual.name, progress: manual.progress };
  } else if (manual.enabled === false) book = { enabled: false, label: labels.book };
  else throw new Error('book.json يتطلب enabled وname وprogress');
} catch (error) { warning('الكتاب', error); }

let show = { enabled: false, label: labels.show, ...(previous.show ?? {}) };
try {
  if (!config.traktUsername || !process.env.TRAKT_CLIENT_ID) throw new Error('أضف traktUsername وTRAKT_CLIENT_ID');
  const history = await request(`https://api.trakt.tv/users/${encodeURIComponent(config.traktUsername)}/history/episodes?limit=1`, {
    headers: { 'trakt-api-version': '2', 'trakt-api-key': process.env.TRAKT_CLIENT_ID, 'Content-Type': 'application/json' }
  });
  const item = history[0];
  if (!item?.show?.title || !Number.isFinite(item.episode?.season) || !Number.isFinite(item.episode?.number)) throw new Error('استجابة Trakt لا تحتوي على حلقة مكتملة');
  show = { enabled: true, label: labels.show, name: item.show.title, episode: `S${item.episode.season} E${item.episode.number}`, watchedAt: item.watched_at ?? new Date().toISOString() };
} catch (error) { warning('المسلسل', error); }

let chess = previous.chess ?? {};
try {
  if (!config.chessUsername) throw new Error('chessUsername غير موجود في config.json');
  const stats = await request(`https://api.chess.com/pub/player/${encodeURIComponent(config.chessUsername)}/stats`, { headers: { 'User-Agent': 'life-dashboard-activity-updater/1.0' } });
  const rating = stats.chess_rapid?.last?.rating;
  if (!Number.isFinite(rating)) throw new Error('تقييم rapid غير موجود');
  chess = { username: config.chessUsername, rating };
} catch (error) { warning('الشطرنج', error); }

let github = previous.github ?? {};
try {
  if (!config.githubUsername) throw new Error('githubUsername غير موجود في config.json');
  const repos = await request(`https://api.github.com/users/${encodeURIComponent(config.githubUsername)}/repos?sort=updated&per_page=1`, {
    headers: { Accept: 'application/vnd.github+json', ...(process.env.GITHUB_TOKEN ? { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` } : {}) }
  });
  const repo = repos[0];
  if (!repo?.name || !repo.html_url) throw new Error('لم يُعثر على مستودع');
  github = { username: config.githubUsername, repoName: repo.name, repoUrl: repo.html_url };
} catch (error) { warning('GitHub', error); }

const output = { updatedAt: new Date().toISOString(), book, show, chess, github };
await writeFile(path.join(root, 'activity.json'), `${JSON.stringify(output, null, 2)}\n`);
console.log('تم تحديث activity.json.');
