/**
 * MaricaCity - Dropdown Login Handler
 * Handles AJAX-based login with in-place feedback in dropdown
 */

document.addEventListener('DOMContentLoaded', function () {
  // Prevent dropdowns from closing when clicking inside
  const loginDropdowns = document.querySelectorAll('.dropdown-menu');
  loginDropdowns.forEach(dropdown => {
    dropdown.addEventListener('click', function (e) {
      e.stopPropagation();
    });
  });

  // Find all login forms (from different dropdowns)
  const loginForms = document.querySelectorAll('form[action*="accounts/login"]');

  loginForms.forEach(form => {
    form.addEventListener('submit', async function (e) {
      e.preventDefault();

      const submitButton = form.querySelector('button[type="submit"]');
      const originalButtonText = submitButton.textContent;
      const formId = form.id;

      // Disable form during submission
      submitButton.disabled = true;
      submitButton.innerHTML =
        '<span class="spinner-border spinner-border-sm me-2"></span>Entrando...';

      // Remove any existing error messages
      const existingError = form.querySelector('.alert-danger');
      if (existingError) {
        existingError.remove();
      }

      // Get form data
      const formData = new FormData(form);

      try {
        const response = await fetch(form.action, {
          method: 'POST',
          body: formData,
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
          },
        });

        const data = await response.json();

        if (data.success) {
          // Success - close dropdown and reload page to show logged-in state
          submitButton.innerHTML = '<i class="bi bi-check-circle me-2"></i>Sucesso!';
          submitButton.classList.remove('btn-dark');
          submitButton.classList.add('btn-success');

          // Close the dropdown
          const dropdown = form.closest('.dropdown-menu');
          if (dropdown) {
            const dropdownToggle = dropdown.previousElementSibling;
            if (dropdownToggle && bootstrap && bootstrap.Dropdown) {
              const bsDropdown = bootstrap.Dropdown.getInstance(dropdownToggle);
              if (bsDropdown) {
                bsDropdown.hide();
              }
            }
          }

          // Reload page after short delay
          setTimeout(() => {
            location.reload();
          }, 500);
        } else {
          // Error - show error message in the form
          showErrorInForm(form, data.error || 'Erro ao fazer login.');

          // Re-enable form
          submitButton.disabled = false;
          submitButton.textContent = originalButtonText;
        }
      } catch (error) {
        console.error('Login error:', error);
        showErrorInForm(form, 'Erro ao conectar com o servidor. Tente novamente.');

        // Re-enable form
        submitButton.disabled = false;
        submitButton.textContent = originalButtonText;
      }
    });
  });
});

/**
 * Display error message within the form
 * @param {HTMLFormElement} form - The form element
 * @param {string} message - Error message to display
 */
function showErrorInForm(form, message) {
  // Remove any existing error
  const existingError = form.querySelector('.alert-danger');
  if (existingError) {
    existingError.remove();
  }

  // Create error alert
  const errorDiv = document.createElement('div');
  errorDiv.className = 'alert alert-danger alert-dismissible fade show mb-3';
  errorDiv.setAttribute('role', 'alert');
  errorDiv.innerHTML = `
    <i class="bi bi-exclamation-triangle me-2"></i>${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;

  // Insert at the beginning of the form
  form.insertBefore(errorDiv, form.firstChild);

  // Shake animation for error
  form.style.animation = 'shake 0.3s ease';
  setTimeout(() => {
    form.style.animation = '';
  }, 300);
}

// Add shake animation CSS if not already present
if (!document.getElementById('login-shake-styles')) {
  const style = document.createElement('style');
  style.id = 'login-shake-styles';
  style.textContent = `
    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      25% { transform: translateX(-10px); }
      75% { transform: translateX(10px); }
    }
  `;
  document.head.appendChild(style);
}
