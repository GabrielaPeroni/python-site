/**
 * MaricaCity - Shared Utilities
 * Common functions used across the application
 */

/**
 * Get CSRF token from cookie
 * @param {string} name - Cookie name
 * @returns {string|null} Cookie value
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

// Export for use in other scripts
if (typeof window !== 'undefined') {
  window.getCookie = getCookie;
}
