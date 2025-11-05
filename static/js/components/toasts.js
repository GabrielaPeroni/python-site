/**
 * MaricaCity - Componente de Toast
 * Mostra automaticamente mensagens de toast do Bootstrap
 */

document.addEventListener('DOMContentLoaded', function () {
  const toastElList = [].slice.call(document.querySelectorAll('.toast'));
  const toastList = toastElList.map(function (toastEl) {
    return new bootstrap.Toast(toastEl);
  });
  toastList.forEach(toast => toast.show());
});
