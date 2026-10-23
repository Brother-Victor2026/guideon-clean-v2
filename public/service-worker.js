self.addEventListener('install', event => { self.skipWaiting(); });
self.addEventListener('activate', event => { event.waitUntil(self.clients.claim()); });

self.addEventListener('push', event => {
  let d = {};
  try { d = event.data ? event.data.json() : {}; } catch (e) { d = { body: event.data ? event.data.text() : '' }; }
  event.waitUntil((async () => {
    if (d.topic === 'replies') {
      const list = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
      if (list.some(c => c.visibilityState === 'visible')) return;
    }
    await self.registration.showNotification(d.title || 'Guidéon', {
      body: d.body || '',
      icon: '/icon-192.png',
      badge: '/badge-96.png',
      tag: d.tag || ('g-' + Date.now()),
      vibrate: [200, 100, 200],
      data: { url: d.url || '/' },
      actions: d.installAction ? [{ action: 'install', title: '📲 Installer' }] : (d.updateAction ? [{ action: 'verify', title: '🔄 Vérifier' }] : [])
    });
  })());
});

self.addEventListener('notificationclick', event => {
  event.notification.close();
  const data = event.notification.data || {};
  const wantActivate = event.action === 'activate' || data.activate === true;
  const wantInstall = event.action === 'install';
  const wantVerify = event.action === 'verify';
  const url = wantActivate ? '/?activerNotifs=1' : (wantInstall ? '/?triggerInstall=1' : (data.url || '/'));
  event.waitUntil(self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(list => {
    for (const c of list) {
      if ('focus' in c) {
        if (wantActivate) c.postMessage({ type: 'ACTIVATE_REPLIES' });
        if (wantInstall) c.postMessage({ type: 'TRIGGER_INSTALL' });
        if (wantVerify) c.postMessage({ type: 'RELOAD_PAGE' });
        return c.focus();
      }
    }
    return self.clients.openWindow(url);
  }));
});

self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SHOW_NOTIFICATION' && event.data.force === true) {
    self.registration.showNotification('Guidéon', { body: event.data.message || '', icon: '/icon-192.png', badge: '/badge-96.png', tag: 'guideon-local' });
  }
});
self.addEventListener('fetch', function(){});
