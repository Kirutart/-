const CACHE_PREFIX = 'last-lesson-static-';
const CACHE_NAME = `${CACHE_PREFIX}v7.25`;
const APP_SHELL = [
  './assets/ui/main-menu-background-v2-1080x1920.webp',
  './assets/ui/circle-select-background-v3-744x2114.webp',
  './assets/ui/records-background-v3-1440x2560.png',
  './assets/ui/story-dialog-frame-v2.webp',
  './assets/ui/perk-upgrade-background-v2-841x1870.webp',
  './assets/ui/perk-icons/chalk_count.webp',
  './assets/ui/perk-icons/chalk_dmg.webp',
  './assets/ui/perk-icons/chalk_cd.webp',
  './assets/ui/perk-icons/chalk_pierce.webp',
  './assets/ui/perk-icons/chalk_ricochet.webp',
  './assets/ui/perk-icons/chalk_split.webp',
  './assets/ui/perk-icons/chalk_control.webp',
  './assets/ui/perk-icons/chalk_ghost.webp',
  './assets/ui/perk-icons/chalk_spirit.webp',
  './assets/ui/perk-icons/ghost_panic.webp',
  './assets/ui/perk-icons/ghost_hysteria.webp',
  './assets/ui/perk-icons/chalk_surprise.webp',
  './assets/story/intro-01.webp',
  './assets/story/intro-02.webp',
  './assets/story/intro-03.webp',
  './assets/game/backgrounds/01_limbo.webp?rev=pixel-v2',
  './assets/game/backgrounds/02_attraction.webp?rev=pixel-v2',
  './assets/game/backgrounds/03_gluttony.webp?rev=pixel-v2',
  './assets/game/backgrounds/04_greed.webp?rev=pixel-v2',
  './assets/game/backgrounds/05_wrath.webp?rev=pixel-v2',
  './assets/game/backgrounds/06_heresy.webp?rev=pixel-v2',
  './assets/game/backgrounds/07_violence.webp?rev=pixel-v2',
  './assets/game/backgrounds/08_fraud.webp?rev=pixel-v2',
  './assets/game/backgrounds/09_treachery.webp?rev=pixel-v2',
  './assets/game/characters/sprites/teacher-human-walk-v1.webp',
  './assets/game/characters/sprites/teacher-demon-2-walk-v1.webp',
  './assets/game/characters/sprites/teacher-demon-3-walk-v1.webp',
  './assets/game/enemies/sprites/first-grader-walk-v1.webp',
  './assets/game/enemies/sprites/middle-schooler-walk-v1.webp',
  './assets/game/enemies/sprites/spitter-walk-v1.webp',
  './assets/game/weapons/pointer-topdown-v1.png',
  './assets/game/weapons/bag-orbit-v1.png',
  './assets/game/pickups/xp-notebook-v1.png',
  './assets/game/pickups/xp-books-v1.png',
  './assets/game/pickups/xp-cigarette-v1.png',
  './assets/game/interwave/pause_01_limbo.webp',
  './assets/fonts/cormorant-unicase/CormorantUnicase-Regular.ttf',
  './assets/fonts/cormorant-unicase/CormorantUnicase-Bold.ttf',
  './assets/fonts/oranienbaum/Oranienbaum-Regular.ttf'
];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(key => key.startsWith(CACHE_PREFIX) && key !== CACHE_NAME).map(key => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== self.location.origin) return;

  if (request.mode === 'navigate') {
    event.respondWith(fetch(request).catch(() => caches.match('./index.html')));
    return;
  }

  if (!['image', 'font'].includes(request.destination)) return;
  event.respondWith(
    caches.open(CACHE_NAME).then(async cache => {
      const cached = await cache.match(request);
      if (cached) return cached;
      const response = await fetch(request);
      if (response.ok) cache.put(request, response.clone());
      return response;
    })
  );
});
