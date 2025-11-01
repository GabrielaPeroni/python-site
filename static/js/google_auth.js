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
  console.log('Signed in as:', payload.email);
  console.log('Full name:', payload.name);
  console.log('Profile image:', payload.picture);

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
