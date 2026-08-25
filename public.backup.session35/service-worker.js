self.addEventListener('install', event => {
  console.log('📱 Service Worker installé');
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  console.log('📱 Service Worker activé');
  self.clients.claim();
});

self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SHOW_NOTIFICATION') {
    self.registration.showNotification('🧠 Guidéon', {
      body: event.data.message || 'Guidéon a répondu!',
      icon: '🧠',
      tag: 'guideon-notification',
      requireInteraction: false
    });
  }
});
