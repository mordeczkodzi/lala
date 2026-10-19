/* Otulka – galeria, wybór wariantu (Kolor × Zestaw), dodawanie do koszyka i lepki pasek. */
(function () {
  'use strict';

  function qs(sel, root) {
    return (root || document).querySelector(sel);
  }

  function qsa(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  function routes() {
    var r = (window.Theme && window.Theme.routes) || {};
    var root = (window.Shopify && window.Shopify.routes && window.Shopify.routes.root) || '/';
    return {
      add: r.cart_add_url || root + 'cart/add.js',
      cart: r.cart_url || root + 'cart'
    };
  }

  function isDrawerOpen() {
    var d = document.querySelector('theme-drawer#cart-drawer');
    return Boolean(d && (d.isOpen || d.hasAttribute('open')));
  }

  /**
   * Dodaje pozycje do koszyka. Korzysta z Shopify.actions (odświeża i otwiera szufladę koszyka motywu),
   * a gdy to niedostępne – z AJAX API i przejścia do /cart.
   * @param {{id: number, quantity: number}[]} lines
   */
  function addToCart(lines) {
    var actions = window.Shopify && window.Shopify.actions;

    function viaAjax() {
      return fetch(routes().add, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ items: lines })
      }).then(function (res) {
        return res.json().then(function (body) {
          if (!res.ok) throw new Error(body.description || body.message || 'add_failed');
          window.location.href = routes().cart;
        });
      });
    }

    if (!actions || typeof actions.updateCart !== 'function') return viaAjax();

    return actions
      .updateCart(
        {
          lines: lines.map(function (l) {
            return { merchandiseId: 'gid://shopify/ProductVariant/' + l.id, quantity: l.quantity };
          })
        },
        { event: { context: 'product' } }
      )
      .then(
        function (result) {
          if (result && result.userErrors && result.userErrors.length) {
            throw new Error(result.userErrors[0].message);
          }
          setTimeout(function () {
            if (!isDrawerOpen() && typeof actions.openCart === 'function') actions.openCart();
          }, 200);
        },
        function (error) {
          if (error && error.name === 'AbortError') throw error;
          return viaAjax();
        }
      );
  }

  function initGallery(root) {
    var track = qs('[data-otk-track]', root);
    if (!track) return { goToMedia: function () {} };

    var slides = qsa('[data-otk-slide]', track);
    var thumbsWrap = qs('[data-otk-thumbs]', root);
    var thumbs = qsa('[data-otk-thumb]', root);
    var counter = qs('[data-otk-count]', root);
    var ticking = false;

    function index() {
      return Math.round(track.scrollLeft / Math.max(track.clientWidth, 1));
    }

    function go(i, smooth) {
      i = Math.max(0, Math.min(slides.length - 1, i));
      track.scrollTo({ left: i * track.clientWidth, behavior: smooth === false ? 'auto' : 'smooth' });
    }

    function sync() {
      ticking = false;
      var i = index();
      if (counter) counter.textContent = i + 1 + ' / ' + slides.length;
      thumbs.forEach(function (t, n) {
        if (n === i) {
          t.setAttribute('aria-current', 'true');
          if (thumbsWrap) {
            var target = t.offsetLeft - (thumbsWrap.clientWidth - t.clientWidth) / 2;
            thumbsWrap.scrollTo({ left: target, behavior: 'smooth' });
          }
        } else {
          t.removeAttribute('aria-current');
        }
      });
    }

    track.addEventListener(
      'scroll',
      function () {
        if (!ticking) {
          ticking = true;
          requestAnimationFrame(sync);
        }
      },
      { passive: true }
    );

    thumbs.forEach(function (t) {
      t.addEventListener('click', function () {
        go(parseInt(t.getAttribute('data-otk-thumb'), 10));
      });
    });

    var prev = qs('[data-otk-prev]', root);
    var next = qs('[data-otk-next]', root);
    if (prev) prev.addEventListener('click', function () { go(index() - 1); });
    if (next) next.addEventListener('click', function () { go(index() + 1); });

    return {
      goToMedia: function (mediaId) {
        for (var i = 0; i < slides.length; i++) {
          if (slides[i].getAttribute('data-media-id') === String(mediaId)) {
            go(i);
            return;
          }
        }
      }
    };
  }

  function initHero(root) {
    if (root.__otk) return;
    root.__otk = true;

    var dataEl = qs('[data-otk-json]', root);
    if (!dataEl) return;
    var data = JSON.parse(dataEl.textContent);
    var variants = data.variants || [];
    var state = { o1: data.o1, o2: data.o2 };
    var gallery = initGallery(root);
    var form = qs('[data-otk-form]', root);
    var idInput = qs('[data-otk-id]', root);
    var mainBtn = qs('[data-otk-main]', root);
    var addonCb = qs('[data-otk-addon-cb]', root);
    var sticky = qs('[data-otk-sticky]', root);

    // Lepki pasek przenosimy do <body>, żeby position: fixed nie zależało od przodków sekcji.
    if (sticky) {
      qsa('body > [data-otk-sticky]').forEach(function (old) {
        old.remove();
      });
      document.body.appendChild(sticky);
    }

    function find(o1, o2) {
      for (var i = 0; i < variants.length; i++) {
        if (variants[i].o1 === o1 && variants[i].o2 === o2) return variants[i];
      }
      return null;
    }

    function setText(sel, text, scope) {
      qsa(sel, scope || root).forEach(function (el) {
        el.textContent = text;
      });
    }

    function toggle(sel, show, scope) {
      qsa(sel, scope || root).forEach(function (el) {
        el.hidden = !show;
      });
    }

    function render(scrollToImage) {
      var v = find(state.o1, state.o2);

      setText('[data-otk-color-label]', state.o1);
      setText('[data-otk-bundle-label]', state.o2);

      qsa('[data-otk-swatch]', root).forEach(function (sw) {
        sw.classList.toggle('is-selected', sw.getAttribute('data-otk-swatch') === state.o1);
      });

      qsa('[data-otk-bundle]', root).forEach(function (card) {
        var name = card.getAttribute('data-otk-bundle');
        var bv = find(state.o1, name);
        card.classList.toggle('is-selected', name === state.o2);
        if (!bv) return;
        card.classList.toggle('is-soldout', !bv.av);
        setText('[data-otk-bprice]', bv.pf, card);
        setText('[data-otk-bcompare]', bv.cf, card);
        toggle('[data-otk-bcompare]', Boolean(bv.cf), card);
        setText('[data-otk-bsave]', bv.sf ? data.t.save + ' ' + bv.sf : '', card);
        toggle('[data-otk-bsave]', Boolean(bv.sf), card);
        var img = qs('.otk-bundle__img img', card);
        if (img && bv.img) img.src = bv.img;
      });

      var belt = find(state.o1, data.addon);
      var addon = qs('[data-otk-addon]', root);
      if (addon) {
        addon.hidden = !(belt && belt.av);
        if (belt) setText('[data-otk-addon-price]', belt.pf, addon);
      }

      if (!v) return;

      if (idInput) idInput.value = v.id;
      setText('[data-otk-price]', v.pf);
      setText('[data-otk-compare]', v.cf);
      toggle('[data-otk-compare]', Boolean(v.cf));
      setText('[data-otk-pct]', v.pct ? '-' + v.pct + '%' : '');
      toggle('[data-otk-pct]', v.pct > 0);

      var buttons = qsa('[data-otk-submit]', root).concat(sticky ? qsa('[data-otk-submit]', sticky) : []);
      buttons.forEach(function (b) {
        b.disabled = !v.av;
        var label = qs('[data-otk-cta-label]', b);
        if (label) label.textContent = v.av ? b.getAttribute('data-label') || data.t.add : data.t.soldout;
        var price = qs('[data-otk-cta-price]', b);
        if (price) {
          price.textContent = v.pf;
          price.hidden = !v.av;
        }
      });

      if (sticky) {
        setText('[data-otk-sticky-variant]', v.o1 + ' / ' + v.o2, sticky);
        setText('[data-otk-sticky-price]', v.pf, sticky);
        setText('[data-otk-sticky-compare]', v.cf, sticky);
        toggle('[data-otk-sticky-compare]', Boolean(v.cf), sticky);
        var simg = qs('.otk-sticky__img', sticky);
        if (simg && v.img) simg.src = v.img;
      }

      if (scrollToImage && v.m) gallery.goToMedia(v.m);

      try {
        var url = new URL(window.location.href);
        url.searchParams.set('variant', v.id);
        window.history.replaceState(window.history.state, '', url.toString());
      } catch (e) {
        /* brak wsparcia URL – pomijamy */
      }
    }

    qsa('[data-otk-color]', root).forEach(function (input) {
      input.addEventListener('change', function () {
        state.o1 = input.value;
        render(true);
      });
    });

    qsa('[data-otk-bundle-input]', root).forEach(function (input) {
      input.addEventListener('change', function () {
        state.o2 = input.value;
        render(false);
      });
    });

    function submit(btn) {
      var v = find(state.o1, state.o2);
      if (!v || !v.av) return;
      var lines = [{ id: v.id, quantity: 1 }];
      var belt = find(state.o1, data.addon);
      if (addonCb && addonCb.checked && belt && belt.av) lines.push({ id: belt.id, quantity: 1 });

      btn.classList.add('is-loading');
      btn.setAttribute('aria-busy', 'true');
      addToCart(lines)
        .catch(function (error) {
          if (error && error.name === 'AbortError') return;
          window.alert(data.t.error + (error && error.message ? '\n' + error.message : ''));
        })
        .then(function () {
          btn.classList.remove('is-loading');
          btn.removeAttribute('aria-busy');
          if (addonCb) addonCb.checked = false;
        });
    }

    if (form) {
      form.addEventListener('submit', function (event) {
        event.preventDefault();
        submit(mainBtn || form.querySelector('[type="submit"]'));
      });
    }

    if (sticky) {
      var stickyBtn = qs('[data-otk-submit]', sticky);
      if (stickyBtn) {
        stickyBtn.addEventListener('click', function () {
          submit(stickyBtn);
        });
      }

      var setSticky = function (show) {
        sticky.classList.toggle('is-visible', show);
        if (show) {
          sticky.removeAttribute('inert');
          sticky.removeAttribute('aria-hidden');
        } else {
          sticky.setAttribute('inert', '');
          sticky.setAttribute('aria-hidden', 'true');
        }
      };

      // Pasek pokazujemy, gdy główny przycisk jest już nad ekranem. Sprawdzamy przy każdym przewinięciu,
      // bo IntersectionObserver nie zgłasza szybkiego „przeskoczenia” przycisku (fling, skok do kotwicy).
      if (mainBtn) {
        var stickyTicking = false;
        var checkSticky = function () {
          stickyTicking = false;
          setSticky(mainBtn.getBoundingClientRect().bottom < 0);
        };
        window.addEventListener(
          'scroll',
          function () {
            if (!stickyTicking) {
              stickyTicking = true;
              requestAnimationFrame(checkSticky);
            }
          },
          { passive: true }
        );
        checkSticky();
      }
    }

    // Linki „wybierz zestaw” z innych sekcji: przewijają do koszyka i zaznaczają zestaw.
    document.addEventListener('click', function (event) {
      var link = event.target.closest ? event.target.closest('[data-otk-pick]') : null;
      if (!link) return;
      var name = link.getAttribute('data-otk-pick');
      qsa('[data-otk-bundle-input]', root).forEach(function (input) {
        if (input.value === name && !input.checked) {
          input.checked = true;
          state.o2 = name;
          render(false);
        }
      });
    });

    render(false);
  }

  function boot() {
    qsa('[data-otk-hero]').forEach(initHero);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  document.addEventListener('shopify:section:load', boot);
})();
