// i18n.js — bilingual EN/PT toggle, shared by all pages.
// PT is the HTML default; put English in a data-en="..." attribute on any element
// (its innerHTML is swapped). For JS-built text, read window.LANG ('pt'|'en') and
// define window.onLangChange to re-render. Persisted in localStorage 'atlas_lang'.
(function () {
  function cur() { try { return localStorage.getItem('atlas_lang') || 'pt'; } catch (e) { return 'pt'; } }
  function apply() {
    var en = cur() === 'en';
    window.LANG = en ? 'en' : 'pt';
    document.querySelectorAll('[data-en]').forEach(function (el) {
      if (el.getAttribute('data-pt') === null) el.setAttribute('data-pt', el.innerHTML);
      el.innerHTML = en ? el.getAttribute('data-en') : el.getAttribute('data-pt');
    });
    document.querySelectorAll('[data-en-ph]').forEach(function (el) {
      if (el.getAttribute('data-pt-ph') === null) el.setAttribute('data-pt-ph', el.getAttribute('placeholder') || '');
      el.setAttribute('placeholder', en ? el.getAttribute('data-en-ph') : el.getAttribute('data-pt-ph'));
    });
    var b = document.getElementById('lang');
    if (b) b.textContent = en ? 'PT' : 'EN';
    document.documentElement.lang = en ? 'en' : 'pt-BR';
    if (typeof window.onLangChange === 'function') window.onLangChange(window.LANG);
  }
  window.applyLang = apply;
  function wire() {
    var b = document.getElementById('lang');
    if (b) b.onclick = function () {
      try { localStorage.setItem('atlas_lang', cur() === 'pt' ? 'en' : 'pt'); } catch (e) {}
      apply();
    };
    apply();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', wire);
  else wire();
})();
