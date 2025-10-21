"""
Custom rate limit handlers for better user experience
"""

from django.contrib import messages
from django.shortcuts import redirect


def ratelimited_error(request, exception):
    """
    Custom handler for rate limit exceeded errors
    Shows a user-friendly message instead of a generic error
    """
    messages.error(
        request,
        "Você excedeu o limite de requisições. Por favor, aguarde alguns minutos antes de tentar novamente.",
    )

    # Redirect to the explore page
    return redirect("explore:explore")
