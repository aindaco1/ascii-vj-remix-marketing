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
  const storedLang = window.localStorage.getItem('ascii-vj-lang');
  const pageLang = document.documentElement.lang || 'en';
  const queryLang = initialUrl.searchParams.get('lang');
  const activeLang = queryLang || (docsPath(initialUrl.pathname) ? pageLang : storedLang) || pageLang || 'en';

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

  applyTranslations(activeLang);
  pruneDocsNav(activeLang);

  document.querySelectorAll('[data-language-switcher]').forEach((select) => {
    select.addEventListener('change', () => {
      const locale = select.value || 'en';
      window.localStorage.setItem('ascii-vj-lang', locale);
      window.location.href = targetForLanguage(locale);
    });
  });
})();
