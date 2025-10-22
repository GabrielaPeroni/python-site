from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.accounts.models import User
from apps.explore.models import Category, Place


def landing_view(request):
    # Featured places (newest)
    featured_places = (
        Place.objects.filter(is_approved=True, is_active=True)
        .prefetch_related("images", "categories")
        .order_by("-created_at")[:6]
    )

    # Trending places (most popular in last 30 days - for now just use recently added)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    trending_places = (
        Place.objects.filter(
            is_approved=True, is_active=True, created_at__gte=thirty_days_ago
        )
        .prefetch_related("images", "categories")
        .order_by("-created_at")[:4]
    )

    categories = Category.objects.filter(is_active=True).order_by("display_order")[:8]

    context = {
        "featured_places": featured_places,
        "trending_places": trending_places,
        "categories": categories,
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY,
        "google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
    }
    return render(request, "core/landing.html", context)


def about_view(request):
    """About page view"""
    return render(request, "core/about.html")


@login_required
def admin_dashboard_view(request):
    """Centralized admin dashboard"""
    if not request.user.can_moderate:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect("core:landing")

    # Get key statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    total_places = Place.objects.count()
    pending_places = Place.objects.filter(is_approved=False, is_active=True).count()
    approved_places = Place.objects.filter(is_approved=True).count()

    context = {
        "total_users": total_users,
        "active_users": active_users,
        "total_places": total_places,
        "pending_places": pending_places,
        "approved_places": approved_places,
    }
    return render(request, "core/admin_dashboard.html", context)
