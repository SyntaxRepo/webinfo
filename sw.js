const CACHE_NAME = 'webinfo-cache-v1';
const urlsToCache = [
  '/',
  '/scanner',
  '/geolocation-scanner',
  '/speedtest',
  '/contact',
  'https://cdn.tailwindcss.com',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css',
  '/manifest.json',
  '/icons/logo.png' // Assuming your logo.svg is in an /icons directory
];

// Install event: This is triggered when the service worker is installed.
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache); // Add all the defined URLs to the cache
      })
  );
});

// Fetch event: This is triggered every time the browser requests a resource.
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request) // Try to find the request in the cache
      .then((response) => {
        // If the resource is in the cache, return it
        if (response) {
          return response;
        }
        // Otherwise, fetch it from the network
        return fetch(event.request);
      })
  );
});

// Activate event: This is triggered when the service worker becomes active.
// You might use this to clean up old caches.
self.addEventListener('activate', (event) => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            // Delete old caches
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
