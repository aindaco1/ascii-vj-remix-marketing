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

  function syncDocsMenuState() {
    const nav = document.getElementById('site-nav');
    if (!nav) return;

    const sync = () => {
      document.body.classList.toggle('docs-nav-open', nav.classList.contains('nav-open'));
    };

    sync();
    new MutationObserver(sync).observe(nav, { attributes: true, attributeFilter: ['class'] });
  }

  function initAsciiBackground() {
    if (!document.body.classList.contains('home-shell')) return;

    const layer = document.createElement('pre');
    layer.className = 'ascii-art-background';
    layer.setAttribute('aria-hidden', 'true');
    document.body.insertBefore(layer, document.body.firstChild);

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const ramp = ' .,:;irsXA253hMHGS#9B&@';
    let cols = 0;
    let rows = 0;
    let lastFrame = 0;
    let frameRequest = 0;

    function measure() {
      const style = window.getComputedStyle(layer);
      const fontSize = parseFloat(style.fontSize) || 14;
      const lineHeight = parseFloat(style.lineHeight) || fontSize * 1.1;
      cols = Math.ceil((window.innerWidth * 1.22) / (fontSize * .68));
      rows = Math.ceil((window.innerHeight * 1.2) / lineHeight);
    }

    function glyph(value) {
      const clamped = Math.max(0, Math.min(1, value));
      return ramp[Math.floor(clamped * (ramp.length - 1))];
    }

    function render(time) {
      const loop = (time % 12000) / 12000;
      const wave = loop * Math.PI * 2;
      const lines = [];

      for (let y = 0; y < rows; y += 1) {
        let line = '';
        const normalizedY = y / Math.max(rows - 1, 1);

        for (let x = 0; x < cols; x += 1) {
          const normalizedX = x / Math.max(cols - 1, 1);
          const centerX = normalizedX - .5;
          const centerY = normalizedY - .5;
          const radius = Math.sqrt(centerX * centerX * 1.8 + centerY * centerY);
          const tunnel = Math.sin(radius * 38 - wave * 3.4);
          const diagonal = Math.sin((normalizedX * 11) + (normalizedY * 17) + wave * 2.2);
          const scan = Math.cos((normalizedY * 46) - wave * 5);
          const interference = Math.sin((normalizedX - normalizedY) * 22 + wave * 1.7);
          const envelope = Math.max(0, 1 - radius * 1.35);
          const value = ((tunnel * .46) + (diagonal * .28) + (scan * .16) + (interference * .22)) * envelope + .36;

          line += glyph(value);
        }

        lines.push(line);
      }

      layer.textContent = lines.join('\n');
    }

    function tick(time) {
      if (time - lastFrame > 80) {
        render(time);
        lastFrame = time;
      }
      frameRequest = window.requestAnimationFrame(tick);
    }

    function start() {
      window.cancelAnimationFrame(frameRequest);
      measure();
      render(0);
      if (!reduceMotion.matches) {
        frameRequest = window.requestAnimationFrame(tick);
      }
    }

    start();
    window.addEventListener('resize', start);
    if (typeof reduceMotion.addEventListener === 'function') {
      reduceMotion.addEventListener('change', start);
    } else {
      reduceMotion.addListener(start);
    }
  }

  applyTranslations(activeLang);
  pruneDocsNav(activeLang);
  syncDocsMenuState();
  initAsciiBackground();

  document.querySelectorAll('[data-language-switcher]').forEach((select) => {
    select.addEventListener('change', () => {
      const locale = select.value || 'en';
      window.localStorage.setItem('ascii-vj-lang', locale);
      window.location.href = targetForLanguage(locale);
    });
  });
})();
