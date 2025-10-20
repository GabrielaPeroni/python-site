/**
 * MaricaCity - Favorites Page JavaScript
 * Handles removing favorites with animation
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

document.addEventListener('DOMContentLoaded', function () {
  const favoriteButtons = document.querySelectorAll('.favorite-btn');

  favoriteButtons.forEach(button => {
    button.addEventListener('click', async function (e) {
      e.preventDefault();
      e.stopPropagation();

      const placeId = this.dataset.placeId;
      const isFavorited = this.dataset.favorited === 'true';

      try {
        const response = await fetch(`/explore/place/${placeId}/favorite/toggle/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
          },
        });

        const data = await response.json();

        if (data.success) {
          // Remove the card with animation
          const card = this.closest('.col-12');
          card.style.transition = 'all 0.3s ease';
          card.style.opacity = '0';
          card.style.transform = 'scale(0.9)';

          setTimeout(() => {
            card.remove();

            // Check if no more favorites - reload to show empty state
            if (document.querySelectorAll('.favorite-btn').length === 0) {
              location.reload();
            }
          }, 300);
        }
      } catch (error) {
        console.error('Error toggling favorite:', error);
        alert('Erro ao remover dos favoritos. Tente novamente.');
      }
    });
  });
});
