/**
 * MaricaCity - Place Detail Page JavaScript
 * Handles reviews (create, edit, delete) and favorites functionality
 */

// State variables
let currentReviewId = null;
let deleteReviewId = null;

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
 * Note: Favorite button functionality is now handled by favorites-ui.js
 * which uses localStorage for all users and optionally syncs with backend
 * for logged-in users. The unified system is loaded in base.html.
 */

/**
 * Initialize Place Carousel
 */
function initPlaceCarousel() {
  const carousel = document.querySelector('.place-carousel');
  if (!carousel) return;

  const items = carousel.querySelectorAll('.place-carousel-item');
  const prevBtn = carousel.querySelector('.place-carousel-prev');
  const nextBtn = carousel.querySelector('.place-carousel-next');
  const dots = carousel.querySelectorAll('.place-carousel-dot');

  if (items.length <= 1) return; // No need for carousel with single image

  let currentIndex = 0;

  function showSlide(index) {
    // Remove active class from all items and dots
    items.forEach(item => item.classList.remove('active'));
    dots.forEach(dot => dot.classList.remove('active'));

    // Add active class to current item and dot
    items[index].classList.add('active');
    dots[index].classList.add('active');
    currentIndex = index;
  }

  function nextSlide() {
    const newIndex = (currentIndex + 1) % items.length;
    showSlide(newIndex);
  }

  function prevSlide() {
    const newIndex = (currentIndex - 1 + items.length) % items.length;
    showSlide(newIndex);
  }

  // Event listeners
  if (prevBtn) {
    prevBtn.addEventListener('click', prevSlide);
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', nextSlide);
  }

  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => showSlide(index));
  });

  // Keyboard navigation
  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft') prevSlide();
    if (e.key === 'ArrowRight') nextSlide();
  });
}

// Initialize carousel when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initPlaceCarousel);
} else {
  initPlaceCarousel();
}

// Export functions for global use
window.resetReviewForm = resetReviewForm;
window.editReview = editReview;
window.submitReview = submitReview;
window.deleteReview = deleteReview;
window.confirmDeleteReview = confirmDeleteReview;
