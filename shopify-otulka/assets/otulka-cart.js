/* Otulka – „Klienci też kochali” w szufladzie koszyka. Delegowane zdarzenia przeżywają przerysowanie szuflady. */
(function () {
  'use strict';
  if (window.__otkCartUpsell) return;
  window.__otkCartUpsell = true;

  document.addEventListener('change', function (event) {
    var select = event.target.closest ? event.target.closest('[data-otk-up-select]') : null;
    if (!select) return;
    var option = select.options[select.selectedIndex];
    var img = select.closest('[data-otk-up]').querySelector('img');
    if (img && option && option.getAttribute('data-img')) img.src = option.getAttribute('data-img');
  });

  document.addEventListener('click', function (event) {
    var button = event.target.closest ? event.target.closest('[data-otk-up-add]') : null;
    if (!button) return;
    event.preventDefault();

    var card = button.closest('[data-otk-up]');
    var select = card && card.querySelector('[data-otk-up-select]');
    var id = select ? select.value : null;
    if (!id) return;

    button.disabled = true;
    var lines = [{ id: Number(id), quantity: 1 }];
    var root = (window.Shopify && window.Shopify.routes && window.Shopify.routes.root) || '/';

    // Wspólny helper z otulka-global.js przerysowuje szufladę; bez niego – AJAX i przejście do /cart.
    var request =
      window.OtulkaCart && typeof window.OtulkaCart.add === 'function'
        ? window.OtulkaCart.add(lines, card)
        : fetch(root + 'cart/add.js', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
            body: JSON.stringify({ items: lines })
          }).then(function (res) {
            if (!res.ok) throw new Error('add_failed');
            window.location.href = root + 'cart';
          });

    request
      .catch(function (error) {
        window.alert('Nie udało się dodać do koszyka.' + (error && error.message ? '\n' + error.message : ''));
      })
      .then(function () {
        if (document.body.contains(button)) button.disabled = false;
      });
  });
})();
