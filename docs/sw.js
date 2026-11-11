// Offline cache for the launcher page. Only the launcher's own files are served from here.
const CACHE = 'bench-hub-d0f6a8069d';
const FILES = ["./", "index.html", "manifest.webmanifest", "icon-180.png", "icon-192.png", "icon-512.png", "icons/motion-bench.svg", "icons/kinematics-bench.svg", "icons/beam-bench.svg", "icons/spring-bench.svg", "icons/solid-bench.svg", "icons/thermo-bench.svg", "icons/magnet-bench.svg", "icons/amp-bench.svg", "shots/motion-bench-light.webp", "shots/motion-bench-dark.webp", "shots/kinematics-bench-light.webp", "shots/kinematics-bench-dark.webp", "shots/beam-bench-light.webp", "shots/beam-bench-dark.webp", "shots/spring-bench-light.webp", "shots/spring-bench-dark.webp", "shots/solid-bench-light.webp", "shots/solid-bench-dark.webp", "shots/thermo-bench-light.webp", "shots/thermo-bench-dark.webp", "shots/magnet-bench-light.webp", "shots/magnet-bench-dark.webp", "shots/amp-bench-light.webp", "shots/amp-bench-dark.webp"];
const OWN = new Set(FILES.map(f => new URL(f, self.registration.scope).pathname));
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('bench-hub-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET' || u.origin !== self.location.origin || !OWN.has(u.pathname)) return;
  e.respondWith(caches.open(CACHE).then(async c => {
    const hit = await c.match(e.request, { ignoreSearch: true });
    const net = fetch(e.request).then(r => { if (r.ok) c.put(e.request, r.clone()); return r; }).catch(() => hit);
    return hit || net;
  }));
});
