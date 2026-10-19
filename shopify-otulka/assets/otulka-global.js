/* Otulka – na każdej stronie: przycisk „do góry” i linki FAQ, które przewijają do pytań na tej samej stronie. */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function scrollBehavior() {
    return reduceMotion ? 'auto' : 'smooth';
  }

  // Przycisk przenosimy do <body>, żeby position: fixed nie zależało od przodków stopki.
  function initTopButton() {
    var buttons = document.querySelectorAll('[data-otk-top]');
    if (!buttons.length) return;
    // Po przeładowaniu stopki w edytorze nowy przycisk jest jeszcze w stopce – ten wygrywa.
    var btn = buttons[buttons.length - 1];
    Array.prototype.forEach.call(buttons, function (candidate) {
      if (candidate.parentElement !== document.body) btn = candidate;
    });
    Array.prototype.forEach.call(buttons, function (other) {
      if (other !== btn) other.remove();
    });
    if (btn.parentElement !== document.body) document.body.appendChild(btn);
    btn.hidden = false;

    if (btn.__otk) return;
    btn.__otk = true;

    var ticking = false;
    function check() {
      ticking = false;
      var show = window.scrollY > window.innerHeight * 1.2;
      btn.classList.toggle('is-visible', show);
      btn.tabIndex = show ? 0 : -1;
      btn.setAttribute('aria-hidden', show ? 'false' : 'true');
    }

    window.addEventListener(
      'scroll',
      function () {
        if (!ticking) {
          ticking = true;
          requestAnimationFrame(check);
        }
      },
      { passive: true }
    );

    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: scrollBehavior() });
    });

    check();
  }

  function isFaqLink(url) {
    return /\/pages\/faq\/?$/.test(url.pathname) || url.hash === '#faq';
  }

  function closeMenus() {
    Array.prototype.forEach.call(document.querySelectorAll('header-drawer'), function (drawer) {
      if (typeof drawer.close === 'function') {
        try {
          drawer.close();
        } catch (e) {
          /* szuflada już zamknięta */
        }
      }
    });
  }

  // Link „FAQ” (menu, stopka) nie przenosi na inną stronę, jeśli pytania są już na tej.
  function onFaqClick(event) {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    var link = event.target.closest ? event.target.closest('a[href]') : null;
    if (!link || link.target === '_blank') return;

    var url;
    try {
      url = new URL(link.href, window.location.href);
    } catch (e) {
      return;
    }
    if (url.origin !== window.location.origin || !isFaqLink(url)) return;

    var target = document.getElementById('faq');
    if (!target) return;

    event.preventDefault();
    closeMenus();
    // Szuflada menu blokuje przewijanie, dopóki się nie zamknie – przewijamy w następnej klatce.
    requestAnimationFrame(function () {
      target.scrollIntoView({ behavior: scrollBehavior(), block: 'start' });
    });
  }

  if (!window.__otkGlobal) {
    window.__otkGlobal = true;
    document.addEventListener('click', onFaqClick, true);
    document.addEventListener('shopify:section:load', initTopButton);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTopButton);
  } else {
    initTopButton();
  }
})();
