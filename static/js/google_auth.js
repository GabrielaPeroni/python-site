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

  // 👇 If you plan to authenticate with Django, send the token to the backend:
  /*
  fetch("/auth/google/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"), // if using Django CSRF
    },
    body: JSON.stringify({ token: response.credential }),
  }).then(res => {
    if (res.ok) window.location.href = "/";
  });
  */
}

// Helper function for CSRF if you’ll POST to Django later
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
