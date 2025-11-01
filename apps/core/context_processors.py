"""
Context processors for making variables available to all templates.
"""

from django.conf import settings


def google_oauth(request):
    """
    Add Google OAuth Client ID to template context.
    """
    return {
        "GOOGLE_OAUTH_CLIENT_ID": settings.GOOGLE_OAUTH_CLIENT_ID,
    }
