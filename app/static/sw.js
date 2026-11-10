/* Quizocracy service worker: makes the site installable and shows a friendly page when there is no connection.
 * It caches only the static shell (CSS, JS, icons, the offline page). It never stores a page (pages carry a
 * family's names and progress) or anything under /api/ (answers are checked on the server), so those always go
 * to the network. Static files are kept by their full URL: a new ?v= is a new URL and is fetched fresh.
 * Served at /sw.js (app/routes/extras.py) so that it may look after the whole site. */
const SHELL = 'qz-shell-v1';
const OFFLINE = '/static/offline.html';
const PRECACHE = [OFFLINE, '/static/img/icon-192.png', '/static/img/favicon-32.png'];
const KEEP = /\.(css|js|png|svg|webp|ico|webmanifest|woff2?)$/;     // static files worth keeping (not audio)

self.addEventListener('install', e => {
  e.waitUntil(caches.open(SHELL).then(c => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== SHELL).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;                         // fonts and anything else: the browser's own way
  if (req.mode === 'navigate') {
    // A page: always from the network, never stored. Offline, the offline page stands in.
    e.respondWith(fetch(req).catch(() => caches.match(OFFLINE)));
    return;
  }
  if (!url.pathname.startsWith('/static/') || !KEEP.test(url.pathname)) return;   // /api/ and the rest: untouched
  if (url.searchParams.has('v')) {
    // Versioned (?v=12): this exact URL never changes, so the cached copy is right.
    e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(res => keep(req, res))));
  } else {
    // Unversioned (icons, pictures): answer from the cache at once and refresh it in the background.
    e.respondWith(caches.match(req).then(hit => {
      const net = fetch(req).then(res => keep(req, res)).catch(() => hit);
      return hit || net;
    }));
  }
});

function keep(req, res) {
  if (res && res.ok && res.type === 'basic') {
    const copy = res.clone(), path = new URL(req.url).pathname;
    caches.open(SHELL).then(async c => {
      // one copy per file: a new ?v= replaces the old version
      for (const k of await c.keys()) if (new URL(k.url).pathname === path && k.url !== req.url) c.delete(k);
      return c.put(req, copy);
    });
  }
  return res;
}
