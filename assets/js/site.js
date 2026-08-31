(() => {
  document.documentElement.classList.add('js-ready');

  const translationsEl = document.getElementById('site-translations');
  let translations = {};
  try {
    translations = translationsEl ? JSON.parse(translationsEl.textContent || '{}') : {};
  } catch (_error) {
    translations = {};
  }

  const docsPath = (path) => path === '/docs' || path.startsWith('/docs/') || path === '/es/docs' || path.startsWith('/es/docs/');
  const initialUrl = new URL(window.location.href);
  const pageLang = document.documentElement.lang || 'en';
  const queryLang = initialUrl.searchParams.get('lang');
  const activeLang = queryLang || pageLang || 'en';

  function valueForKey(locale, key) {
    return key.split('.').reduce((value, part) => value && value[part], translations[locale]);
  }

  function applyTranslations(locale) {
    const fallback = 'en';
    document.querySelectorAll('[data-i18n]').forEach((node) => {
      const key = node.getAttribute('data-i18n');
      const value = valueForKey(locale, key) || valueForKey(fallback, key);
      if (typeof value === 'string') node.textContent = value;
    });
    document.querySelectorAll('[data-language-switcher]').forEach((select) => {
      select.value = locale;
    });
    if (!docsPath(window.location.pathname)) {
      document.documentElement.lang = locale;
    }
  }

  function targetForLanguage(locale) {
    const url = new URL(window.location.href);
    if (docsPath(url.pathname)) {
      if (locale === 'es' && !url.pathname.startsWith('/es/')) {
        url.pathname = '/es' + url.pathname;
      } else if (locale === 'en' && url.pathname.startsWith('/es/docs/')) {
        url.pathname = url.pathname.replace(/^\/es/, '');
      }
      url.searchParams.delete('lang');
      return url.toString();
    }
    if (locale === 'es') {
      if (!url.pathname.startsWith('/es/')) {
        url.pathname = '/es' + url.pathname;
      }
      url.searchParams.delete('lang');
      return url.toString();
    }
    if (locale === 'en' && url.pathname.startsWith('/es/')) {
      url.pathname = url.pathname.replace(/^\/es/, '') || '/';
    }
    url.searchParams.delete('lang');
    return url.toString();
  }

  function pruneDocsNav(locale) {
    const nav = document.getElementById('site-nav');
    if (!nav) return;
    const hiddenPrefix = locale === 'es' ? '/docs/' : '/es/';
    nav.querySelectorAll(`.nav-list-item a[href^="${hiddenPrefix}"]`).forEach((link) => {
      const item = link.closest('.nav-list-item');
      if (item) item.remove();
    });
  }

  function syncDocsMenuState() {
    const nav = document.getElementById('site-nav');
    if (!nav) return;

    const sync = () => {
      document.body.classList.toggle('docs-nav-open', nav.classList.contains('nav-open'));
    };

    sync();
    new MutationObserver(sync).observe(nav, { attributes: true, attributeFilter: ['class'] });
  }

  function desktopPlatform() {
    const clientPlatform = navigator.userAgentData && navigator.userAgentData.platform;
    const signature = `${clientPlatform || ''} ${navigator.platform || ''} ${navigator.userAgent || ''}`.toLowerCase();

    if (/iphone|ipad|ipod|android|cros/.test(signature)) return '';
    if (/macintosh|macintel|macppc|mac68k|macos|mac os/.test(signature)) return 'macos';
    if (/windows|win32|win64|wince/.test(signature)) return 'windows';
    if (/linux|x11/.test(signature)) return 'linux';
    return '';
  }

  function configureLatestDownloads() {
    const platform = desktopPlatform();
    if (!platform) return;

    document.querySelectorAll('[data-download-latest]').forEach((link) => {
      const platformUrl = link.getAttribute(`data-download-${platform}`);
      if (!platformUrl) return;
      link.href = platformUrl;
      link.setAttribute('data-download-detected', platform);
    });
  }

  applyTranslations(activeLang);
  pruneDocsNav(activeLang);
  syncDocsMenuState();
  configureLatestDownloads();

  document.querySelectorAll('[data-language-switcher]').forEach((select) => {
    select.addEventListener('change', () => {
      const locale = select.value || 'en';
      window.location.href = targetForLanguage(locale);
    });
  });
})();
