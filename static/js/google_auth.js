function decodeJWT(token) {
  let base64Url = token.split('.')[1];
  let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  let jsonPayload = decodeURIComponent(
    atob(base64)
      .split('')
      .map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
      })
      .join('')
  );
  return JSON.parse(jsonPayload);
}

function handleCredentialResponse(response) {
  const payload = decodeJWT(response.credential);

  // Send token to backend for authentication
  fetch('/auth/google/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({ token: response.credential }),
  })
    .then(res => {
      if (res.ok) {
        window.location.href = '/';
      } else {
        console.error('Google authentication failed');
        alert('Falha ao autenticar com Google. Por favor, tente novamente.');
      }
    })
    .catch(error => {
      console.error('Error during Google authentication:', error);
      alert('Erro ao conectar com o servidor. Por favor, tente novamente.');
    });
}

// Track if Google Sign-In has been initialized
let googleInitialized = false;

// Initialize Google Sign-In SDK
function initializeGoogleSDK() {
  if (
    typeof google !== 'undefined' &&
    google.accounts &&
    window.GOOGLE_CLIENT_ID &&
    !googleInitialized
  ) {
    try {
      google.accounts.id.initialize({
        client_id: window.GOOGLE_CLIENT_ID,
        callback: handleCredentialResponse,
      });
      googleInitialized = true;
      renderGoogleButton();
    } catch (error) {
      console.error('Error initializing Google Sign-In SDK:', error);
    }
  } else if (!googleInitialized) {
    // If Google SDK not ready yet, try again in 100ms
    setTimeout(initializeGoogleSDK, 100);
  }
}

// Render the Google Sign-In button
function renderGoogleButton() {
  if (!googleInitialized) {
    return;
  }

  const googleButton = document.getElementById('google-signin-button');
  if (googleButton && !googleButton.hasChildNodes()) {
    try {
      google.accounts.id.renderButton(googleButton, {
        type: 'standard',
        theme: 'outline',
        size: 'large',
        text: 'signin_with',
        shape: 'rectangular',
        logo_alignment: 'left',
        width: 280,
      });
    } catch (error) {
      console.error('Error rendering Google Sign-In button:', error);
    }
  }
}

// Listen for dropdown show events to render the button when it becomes visible
document.addEventListener('shown.bs.dropdown', function (event) {
  // Check if this is a login dropdown
  const dropdown = event.target;
  if (dropdown.querySelector('#google-signin-button')) {
    renderGoogleButton();
  }
});

// Start initialization when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeGoogleSDK);
} else {
  initializeGoogleSDK();
}
