/**
 * MaricaCity - Utilitários Compartilhados
 * Funções comuns usadas em toda a aplicação
 */

/**
 * Obter token CSRF do cookie
 * @param {string} name - Nome do cookie
 * @returns {string|null} Valor do cookie
 */
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Exportar para uso em outros scripts
if (typeof window !== 'undefined') {
  window.getCookie = getCookie;
}
