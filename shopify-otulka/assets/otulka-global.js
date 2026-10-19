/* Otulka – na każdej stronie: przycisk „do góry”, linki FAQ przewijające do pytań na tej samej stronie
   i wspólne dodawanie do koszyka (window.OtulkaCart). */
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

  var cartRoot = (window.Shopify && window.Shopify.routes && window.Shopify.routes.root) || '/';

  function cartSectionIds() {
    var ids = [];
    Array.prototype.forEach.call(document.querySelectorAll('cart-items-component[data-section-id]'), function (el) {
      if (ids.indexOf(el.dataset.sectionId) === -1) ids.push(el.dataset.sectionId);
    });
    return ids;
  }

  function loadCartEvents() {
    try {
      return import('@shopify/events').catch(function () {
        return null;
      });
    } catch (e) {
      return Promise.resolve(null);
    }
  }

  function openCartDrawer() {
    var drawer = document.querySelector('theme-drawer#cart-drawer');
    if (!drawer || typeof drawer.open !== 'function') return false;
    if (!drawer.isOpen) drawer.open();
    return true;
  }

  /**
   * Dodaje pozycje do koszyka tak jak formularz produktu motywu: /cart/add.js z HTML-em sekcji szuflady
   * i zdarzenie CartLinesUpdateEvent, na które szuflada się przerysowuje. Potem otwiera szufladę
   * (albo przechodzi do /cart, gdy jej nie ma).
   * @param {{id: number, quantity: number}[]} lines
   * @param {Element} [source] element, z którego wysyłamy zdarzenie
   */
  function addToCart(lines, source) {
    var sectionIds = cartSectionIds();
    var itemCount = lines.reduce(function (sum, line) {
      return sum + line.quantity;
    }, 0);

    return loadCartEvents().then(function (events) {
      var LinesEvent = events && events.CartLinesUpdateEvent;
      var deferred = LinesEvent && typeof LinesEvent.createPromise === 'function' ? LinesEvent.createPromise() : null;

      if (deferred) {
        (source || document).dispatchEvent(
          new LinesEvent({
            action: 'add',
            context: 'product',
            lines: lines.map(function (line) {
              return { merchandiseId: String(line.id), quantity: line.quantity };
            }),
            promise: deferred.promise
          })
        );
      }

      function fetchCart() {
        return fetch(cartRoot + 'cart.js', { headers: { Accept: 'application/json' }, credentials: 'same-origin' }).then(
          function (res) {
            return res.json();
          }
        );
      }

      return fetch(cartRoot + 'cart/add.js', {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ items: lines, sections: sectionIds.join(','), sections_url: window.location.pathname })
      })
        .then(function (res) {
          return res.json().then(function (body) {
            return { ok: res.ok && !body.status, body: body };
          });
        })
        .then(function (result) {
          return fetchCart().then(function (cart) {
            if (deferred) {
              deferred.resolve({
                cart: typeof LinesEvent.createCartFromAjaxResponse === 'function' ? LinesEvent.createCartFromAjaxResponse(cart) : cart,
                detail: {
                  items: cart.items,
                  sections: result.ok ? result.body.sections : undefined,
                  didError: !result.ok,
                  source: 'otulka',
                  itemCount: itemCount
                }
              });
            }
            if (!result.ok) throw new Error(result.body.description || result.body.message || 'add_failed');
            return cart;
          });
        })
        .then(
          function (cart) {
            if (!deferred) {
              window.location.href = cartRoot + 'cart';
              return cart;
            }
            // Szuflada przerysowuje się w then() zdarzenia – otwieramy ją chwilę później, już z produktem.
            setTimeout(function () {
              if (!openCartDrawer()) window.location.href = cartRoot + 'cart';
            }, 80);
            return cart;
          },
          function (error) {
            if (deferred) deferred.reject(error);
            throw error;
          }
        );
    });
  }

  window.OtulkaCart = { add: addToCart, open: openCartDrawer };

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
