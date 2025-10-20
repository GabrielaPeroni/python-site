/**
 * MaricaCity - Place Detail Page JavaScript
 * Handles reviews (create, edit, delete) and favorites functionality
 */

// State variables
let currentReviewId = null;
let deleteReviewId = null;

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

/**
 * Reset review form to create new review state
 */
function resetReviewForm() {
  currentReviewId = null;
  const form = document.getElementById('reviewForm');
  const reviewIdField = document.getElementById('reviewId');
  const modalLabel = document.getElementById('reviewModalLabel');
  const submitButtonText = document.getElementById('submitButtonText');

  if (form) form.reset();
  if (reviewIdField) reviewIdField.value = '';
  if (modalLabel) modalLabel.textContent = 'Escrever Avaliação';
  if (submitButtonText) submitButtonText.textContent = 'Enviar Avaliação';
}

/**
 * Populate form for editing existing review
 * @param {number} reviewId - Review ID
 * @param {number} rating - Rating value (1-5)
 * @param {string} comment - Review comment
 */
function editReview(reviewId, rating, comment) {
  currentReviewId = reviewId;

  const reviewIdField = document.getElementById('reviewId');
  const modalLabel = document.getElementById('reviewModalLabel');
  const submitButtonText = document.getElementById('submitButtonText');
  const ratingInput = document.getElementById('rating' + rating);
  const commentField = document.getElementById('reviewComment');

  if (reviewIdField) reviewIdField.value = reviewId;
  if (modalLabel) modalLabel.textContent = 'Editar Avaliação';
  if (submitButtonText) submitButtonText.textContent = 'Atualizar Avaliação';
  if (ratingInput) ratingInput.checked = true;
  if (commentField) commentField.value = comment;
}

/**
 * Submit review (create or update)
 */
function submitReview() {
  const form = document.getElementById('reviewForm');
  if (!form) return;

  const formData = new FormData(form);
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

  if (!csrfToken) {
    alert('Erro: CSRF token não encontrado.');
    return;
  }

  // Determine URL based on whether we're creating or editing
  let url;
  if (currentReviewId) {
    // Get from data attribute on form
    url = form.dataset.editUrlTemplate.replace('0', currentReviewId);
  } else {
    url = form.dataset.createUrl;
  }

  // Submit form via fetch
  fetch(url, {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': csrfToken,
    },
  })
    .then(response => {
      if (response.ok) {
        // Close modal and reload page to show updated review
        const modal = bootstrap.Modal.getInstance(
          document.getElementById('reviewModal')
        );
        if (modal) modal.hide();
        location.reload();
      } else {
        alert('Erro ao enviar avaliação. Por favor, tente novamente.');
      }
    })
    .catch(error => {
      console.error('Error submitting review:', error);
      alert('Erro ao enviar avaliação. Por favor, tente novamente.');
    });
}

/**
 * Show delete confirmation modal
 * @param {number} reviewId - Review ID to delete
 */
function deleteReview(reviewId) {
  deleteReviewId = reviewId;
  const deleteModal = new bootstrap.Modal(document.getElementById('deleteReviewModal'));
  if (deleteModal) deleteModal.show();
}

/**
 * Confirm and execute review deletion
 */
function confirmDeleteReview() {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
  const deleteForm = document.getElementById('deleteReviewForm');

  if (!csrfToken || !deleteForm || !deleteReviewId) {
    alert('Erro ao excluir avaliação.');
    return;
  }

  const url = deleteForm.dataset.deleteUrlTemplate.replace('0', deleteReviewId);

  fetch(url, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken,
    },
  })
    .then(response => {
      if (response.ok) {
        // Close modal and reload page
        const modal = bootstrap.Modal.getInstance(
          document.getElementById('deleteReviewModal')
        );
        if (modal) modal.hide();
        location.reload();
      } else {
        alert('Erro ao excluir avaliação. Por favor, tente novamente.');
      }
    })
    .catch(error => {
      console.error('Error deleting review:', error);
      alert('Erro ao excluir avaliação. Por favor, tente novamente.');
    });
}

/**
 * Initialize favorite button functionality
 * Auto-initializes on DOMContentLoaded
 */
function initializeFavoriteButton() {
  const favoriteBtn = document.getElementById('favoriteBtn');
  if (!favoriteBtn) return;

  const placeId = favoriteBtn.dataset.placeId;
  if (!placeId) return;

  // Add transition
  favoriteBtn.style.transition = 'transform 0.2s ease';

  favoriteBtn.addEventListener('click', async function (e) {
    e.preventDefault();
    e.stopPropagation();

    const isFavorited = this.dataset.favorited === 'true';

    try {
      const csrfToken = getCookie('csrftoken');

      const response = await fetch(`/explore/place/${placeId}/favorite/toggle/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();

      if (data.success) {
        // Update button state
        this.dataset.favorited = data.is_favorited;
        const icon = this.querySelector('i');

        if (data.is_favorited) {
          icon.classList.remove('bi-heart');
          icon.classList.add('bi-heart-fill', 'text-danger');
          this.title = 'Remover dos favoritos';
        } else {
          icon.classList.remove('bi-heart-fill', 'text-danger');
          icon.classList.add('bi-heart');
          this.title = 'Adicionar aos favoritos';
        }

        // Add animation
        this.style.transform = 'scale(1.2)';
        setTimeout(() => {
          this.style.transform = 'scale(1)';
        }, 200);
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
      alert('Erro ao atualizar favorito. Tente novamente.');
    }
  });
}

// Auto-initialize on page load
document.addEventListener('DOMContentLoaded', function () {
  initializeFavoriteButton();
});

// Export functions for global use
window.resetReviewForm = resetReviewForm;
window.editReview = editReview;
window.submitReview = submitReview;
window.deleteReview = deleteReview;
window.confirmDeleteReview = confirmDeleteReview;
