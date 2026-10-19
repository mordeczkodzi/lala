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
    var actions = window.Shopify && window.Shopify.actions;
    var root = (window.Shopify && window.Shopify.routes && window.Shopify.routes.root) || '/';

    function viaAjax() {
      return fetch(root + 'cart/add.js', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ items: [{ id: Number(id), quantity: 1 }] })
      }).then(function (res) {
        if (!res.ok) throw new Error('add_failed');
        window.location.href = root + 'cart';
      });
    }

    var request =
      actions && typeof actions.updateCart === 'function'
        ? actions
            .updateCart(
              { lines: [{ merchandiseId: 'gid://shopify/ProductVariant/' + id, quantity: 1 }] },
              { event: { context: 'cart' } }
            )
            .then(function (result) {
              if (result && result.userErrors && result.userErrors.length) throw new Error(result.userErrors[0].message);
            }, viaAjax)
        : viaAjax();

    request
      .catch(function (error) {
        window.alert('Nie udało się dodać do koszyka.' + (error && error.message ? '\n' + error.message : ''));
      })
      .then(function () {
        if (document.body.contains(button)) button.disabled = false;
      });
  });
})();
