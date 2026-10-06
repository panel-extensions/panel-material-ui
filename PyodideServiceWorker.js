const appName = 'Panel Material UI'
const cachePrefix = appName;
const appCacheName = 'Panel Material UI-0.16.1';

// When set, same-origin requests revalidate with the server instead of trusting the
// browser HTTP cache, so a new worker does not re-cache pages from the previous build.
const fetchCache = null;

const preCacheFiles = [];

const cachePatterns = ['https://cdn.holoviz.org/panel/1.9.4/dist/', 'https://cdn.bokeh.org/bokeh/', 'https://cdn.jsdelivr.net/pyodide/', 'https://files.pythonhosted.org/packages/', 'https://pypi.org/pypi/'];

self.addEventListener('install', (e) => {
  console.log('[Service Worker] Install');
  self.skipWaiting();
  e.waitUntil((async () => {
    const cacheNames = await caches.keys();
    for (const cacheName of cacheNames) {
      if (cacheName.startsWith(cachePrefix) && cacheName !== appCacheName) {
        console.log(`[Service Worker] Delete old cache ${cacheName}`);
        caches.delete(cacheName);
      }
    }
    const cache = await caches.open(appCacheName);
    if (preCacheFiles.length) {
      console.log('[Service Worker] Precaching ');
    }
    preCacheFiles.forEach(async (cacheFile) => {
      const request = new Request(cacheFile);
      const response = await fetch(request);
      if (response.ok || response.type == 'opaque') {
        cache.put(request, response);
      }
    })
  })());
});

self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Activating');
  return self.clients.claim();
});

const networkRequest = (request) => {
  if (!fetchCache || new URL(request.url).origin !== self.location.origin) {
    return request;
  }
  // A navigation request cannot be copied with a RequestInit, so rebuild it by URL.
  if (request.mode === 'navigate') {
    return new Request(request.url, {cache: fetchCache, credentials: request.credentials, redirect: 'manual'});
  }
  return new Request(request, {cache: fetchCache});
};

self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') {
    return
  }
  e.respondWith((async () => {
    const cache = await caches.open(appCacheName);
    let response = await cache.match(e.request);
    console.log(`[Service Worker] Fetching resource: ${e.request.url}`);
    if (response) {
      return response;
    }
    response = await fetch(networkRequest(e.request));
    // Redirects and error pages go back to the page uncached; throwing here turned them
    // into network errors, e.g. a directory URL without its trailing slash.
    if (!response.ok && response.type !== 'opaque') {
      console.log(`[Service Worker] Not caching ${e.request.url}: ${response.type} ${response.status}`);
      return response;
    }
    console.log(`[Service Worker] Caching new resource: ${e.request.url}`);
    if (e.request.mode !== 'no-cors') {
      cache.put(e.request, response.clone());
    }
    return response;
  })());
});