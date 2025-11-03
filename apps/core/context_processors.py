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


def admin_stats(request):
    """
    Add admin statistics to context for sidebar badges.
    Only calculated for authenticated admin users.
    """
    if request.user.is_authenticated and request.user.can_moderate:
        from apps.explore.models import Place
        from apps.news.models import News

        return {
            "pending_places": Place.objects.filter(
                is_approved=False, is_active=True
            ).count(),
            "draft_news": News.objects.filter(status=News.DRAFT).count(),
        }
    return {"pending_places": 0, "draft_news": 0}
