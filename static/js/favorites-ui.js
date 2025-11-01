/**
 * MaricaCity - Favorites UI Handler
 * Manages UI interactions for favorites using the FavoritesService
 */

/**
 * Update favorite button UI
 * @param {HTMLElement} button - Favorite button element
 * @param {boolean} isFavorited - Current favorited status
 */
function updateFavoriteButton(button, isFavorited) {
  const icon = button.querySelector('i');

  if (isFavorited) {
    // Favorited state
    icon.classList.remove('bi-heart');
    icon.classList.add('bi-heart-fill');
    button.classList.add('favorited');
    button.setAttribute('title', 'Remover dos favoritos');
    button.setAttribute('aria-label', 'Remover dos favoritos');
  } else {
    // Not favorited state
    icon.classList.remove('bi-heart-fill');
    icon.classList.add('bi-heart');
    button.classList.remove('favorited');
    button.setAttribute('title', 'Adicionar aos favoritos');
    button.setAttribute('aria-label', 'Adicionar aos favoritos');
  }

  button.dataset.favorited = isFavorited;
}

/**
 * Update favorites count display
 * @param {number} placeId - Place ID
 * @param {number} delta - Change in count (+1 or -1)
 */
function updateFavoritesCount(placeId, delta) {
  const countElements = document.querySelectorAll(
    `[data-favorites-count-for="${placeId}"]`
  );

  countElements.forEach(element => {
    const currentCount = parseInt(element.textContent) || 0;
    const newCount = Math.max(0, currentCount + delta);
    element.textContent = newCount;
  });
}

/**
 * Initialize favorites UI on page load
 */
function initializeFavoritesUI() {
  // Update all favorite buttons based on localStorage
  const buttons = document.querySelectorAll('.favorite-btn');

  buttons.forEach(button => {
    const placeId = button.dataset.placeId;
    if (placeId) {
      const isFavorited = favoritesService.isFavorited(placeId);
      updateFavoriteButton(button, isFavorited);
    }
  });

  // Update favorites count in navbar/header if exists
  updateNavbarFavoritesCount();

  // If user is logged in, sync with backend
  const isLoggedIn = document.body.dataset.userAuthenticated === 'true';
  if (isLoggedIn) {
    const csrfToken = getCookie('csrftoken');
    favoritesService.loadFromBackend().then(() => {
      // Refresh UI after loading from backend
      buttons.forEach(button => {
        const placeId = button.dataset.placeId;
        if (placeId) {
          const isFavorited = favoritesService.isFavorited(placeId);
          updateFavoriteButton(button, isFavorited);
        }
      });
      updateNavbarFavoritesCount();
    });
  }
}

/**
 * Update favorites count in navbar
 */
function updateNavbarFavoritesCount() {
  const navbarCount = document.querySelector('.favorites-count');
  if (navbarCount) {
    const count = favoritesService.getCount();
    navbarCount.textContent = count;

    // Show/hide badge
    if (count > 0) {
      navbarCount.classList.remove('d-none');
    } else {
      navbarCount.classList.add('d-none');
    }
  }
}

/**
 * Handle favorite button click
 * @param {Event} e - Click event
 */
async function handleFavoriteClick(e) {
  e.preventDefault();
  e.stopPropagation();

  const button = e.currentTarget;
  const placeId = button.dataset.placeId;

  if (!placeId) {
    console.error('No place ID found');
    return;
  }

  // Disable button during processing
  button.disabled = true;

  try {
    // Toggle in localStorage
    const isNowFavorited = favoritesService.toggleFavorite(placeId);

    // Update UI
    updateFavoriteButton(button, isNowFavorited);
    updateFavoritesCount(placeId, isNowFavorited ? 1 : -1);
    updateNavbarFavoritesCount();

    // Show feedback animation
    button.style.transition = 'transform 0.2s ease';
    button.style.transform = 'scale(1.3)';
    setTimeout(() => {
      button.style.transform = 'scale(1)';
    }, 200);

    // If logged in, also sync with backend (optional - fire and forget)
    const isLoggedIn = document.body.dataset.userAuthenticated === 'true';
    if (isLoggedIn) {
      const csrfToken = getCookie('csrftoken');

      // Optional: call backend endpoint to save favorite
      try {
        await fetch(`/explore/place/${placeId}/favorite/toggle/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
          },
        });
      } catch (error) {
        // Backend sync failed but local storage still works
        console.warn('Backend sync failed:', error);
      }
    }
  } catch (error) {
    console.error('Error toggling favorite:', error);
    alert('Erro ao atualizar favorito. Tente novamente.');
  } finally {
    button.disabled = false;
  }
}

/**
 * Handle removing favorite from favorites page
 * @param {Event} e - Click event
 */
async function handleRemoveFavorite(e) {
  e.preventDefault();
  e.stopPropagation();

  const button = e.currentTarget;
  const placeId = button.dataset.placeId;

  if (!placeId) return;

  // Remove from localStorage
  favoritesService.removeFavorite(placeId);

  // Remove card with animation
  const card = button.closest('.col-12, .col-md-6, .col-lg-4');
  if (card) {
    card.style.transition = 'all 0.3s ease';
    card.style.opacity = '0';
    card.style.transform = 'scale(0.9)';

    setTimeout(() => {
      card.remove();

      // Check if no more favorites
      const remainingCards = document.querySelectorAll('.favorite-btn').length;
      if (remainingCards === 0) {
        location.reload(); // Reload to show empty state
      }
    }, 300);
  }

  // Update navbar count
  updateNavbarFavoritesCount();

  // Sync with backend if logged in
  const isLoggedIn = document.body.dataset.userAuthenticated === 'true';
  if (isLoggedIn) {
    const csrfToken = getCookie('csrftoken');
    try {
      await fetch(`/explore/place/${placeId}/favorite/toggle/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json',
        },
      });
    } catch (error) {
      console.warn('Backend sync failed:', error);
    }
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
  // Initialize UI
  initializeFavoritesUI();

  // Add click handlers to all favorite buttons
  const favoriteButtons = document.querySelectorAll(
    '.favorite-btn:not([data-remove-mode])'
  );
  favoriteButtons.forEach(button => {
    button.addEventListener('click', handleFavoriteClick);
  });

  // Add click handlers for remove buttons on favorites page
  const removeButtons = document.querySelectorAll('.favorite-btn[data-remove-mode]');
  removeButtons.forEach(button => {
    button.addEventListener('click', handleRemoveFavorite);
  });

  // Listen for storage changes from other tabs
  window.addEventListener('storage', function (e) {
    if (e.key === 'marica_favorites') {
      initializeFavoritesUI();
    }
  });
});
