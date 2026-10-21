// Oficina MinuteMark: deja la app lista para abrir sin internet.
// La página se pide primero a la red (así siempre llega la versión nueva) y, sin conexión, sale de la copia.
// Los datos no pasan por aquí: Firestore los guarda en el equipo y los sincroniza solo.
const CACHE = 'oficina-v1';
const BASE = ['./', 'manifest.webmanifest', 'img/mm-logo-white.png', 'img/mm-logo-color.png', 'img/mm-isotipo.png',
  'img/mark-02-saludo.webp', 'img/mark-08-senalando.webp', 'img/mark-10-pulgar-arriba.webp', 'img/icono-180.png', 'img/icono-192.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(BASE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});

function guardar(req, res) {
  if (res && (res.ok || res.type === 'opaque')) { const copia = res.clone(); caches.open(CACHE).then(c => c.put(req, copia)); }
  return res;
}
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const u = new URL(req.url);
  const propio = u.origin === self.location.origin;
  const sdk = u.hostname === 'www.gstatic.com' && u.pathname.startsWith('/firebasejs/');
  const fuente = u.hostname === 'fonts.googleapis.com' || u.hostname === 'fonts.gstatic.com';
  if (propio && (req.mode === 'navigate' || u.pathname.endsWith('/') || u.pathname.endsWith('.html'))) {
    e.respondWith(fetch(req).then(r => guardar(req, r)).catch(() => caches.match(req).then(r => r || caches.match('./'))));
  } else if (propio || sdk || fuente) {
    e.respondWith(caches.match(req).then(r => r || fetch(req).then(x => guardar(req, x))));
  }
});
