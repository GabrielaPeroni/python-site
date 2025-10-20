/**
 * User Management JavaScript
 * Handles AJAX operations for user type updates and status toggles
 */

document.addEventListener('DOMContentLoaded', function () {
  // Get CSRF token from cookie
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

  const csrfToken = getCookie('csrftoken');

  // Handle user type change
  const userTypeSelects = document.querySelectorAll('.user-type-select');
  userTypeSelects.forEach(select => {
    select.addEventListener('change', function () {
      const userId = this.dataset.userId;
      const newType = this.value;
      const originalType = this.querySelector('option[selected]')?.value;

      if (
        !confirm(
          'Tem certeza que deseja alterar o tipo deste usuário?\n\nIsso pode modificar as permissões do usuário no sistema.'
        )
      ) {
        this.value = originalType;
        return;
      }

      // Disable select during request
      this.disabled = true;

      fetch(`/accounts/usuarios/${userId}/tipo/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_type=${newType}`,
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            // Show success message
            showNotification('success', data.message);

            // Update the selected option
            const options = this.querySelectorAll('option');
            options.forEach(opt => {
              opt.removeAttribute('selected');
              if (opt.value === newType) {
                opt.setAttribute('selected', 'selected');
              }
            });
          } else {
            // Revert to original type
            this.value = originalType;
            showNotification(
              'error',
              data.error || 'Erro ao atualizar tipo de usuário'
            );
          }
        })
        .catch(error => {
          console.error('Error:', error);
          this.value = originalType;
          showNotification('error', 'Erro ao processar solicitação');
        })
        .finally(() => {
          this.disabled = false;
        });
    });
  });

  // Handle status toggle
  const statusButtons = document.querySelectorAll('.toggle-status-btn');
  statusButtons.forEach(button => {
    button.addEventListener('click', function () {
      const userId = this.dataset.userId;
      const row = document.getElementById(`user-row-${userId}`);
      const statusBadge = row.querySelector(`.status-badge-${userId}`);
      const isActive = statusBadge.classList.contains('bg-success');

      const action = isActive ? 'desativar' : 'ativar';
      if (!confirm(`Tem certeza que deseja ${action} este usuário?`)) {
        return;
      }

      // Disable button during request
      this.disabled = true;

      fetch(`/accounts/usuarios/${userId}/status/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
        },
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            // Update badge
            if (data.is_active) {
              statusBadge.classList.remove('bg-secondary');
              statusBadge.classList.add('bg-success');
              statusBadge.textContent = 'Ativo';
              this.innerHTML = '<i class="bi bi-x-circle"></i>';
            } else {
              statusBadge.classList.remove('bg-success');
              statusBadge.classList.add('bg-secondary');
              statusBadge.textContent = 'Inativo';
              this.innerHTML = '<i class="bi bi-check-circle"></i>';
            }

            showNotification('success', data.message);
          } else {
            showNotification('error', data.error || 'Erro ao alterar status');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          showNotification('error', 'Erro ao processar solicitação');
        })
        .finally(() => {
          this.disabled = false;
        });
    });
  });

  /**
   * Show notification message
   * @param {string} type - 'success' or 'error'
   * @param {string} message - Message to display
   */
  function showNotification(type, message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${
      type === 'success' ? 'success' : 'danger'
    } alert-dismissible fade show position-fixed`;
    notification.style.cssText =
      'top: 20px; right: 20px; z-index: 9999; min-width: 300px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);';
    notification.innerHTML = `
      <i class="bi bi-${
        type === 'success' ? 'check-circle' : 'exclamation-circle'
      } me-2"></i>
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(notification);

    // Auto-remove after 5 seconds
    setTimeout(() => {
      notification.classList.remove('show');
      setTimeout(() => notification.remove(), 150);
    }, 5000);
  }
});
