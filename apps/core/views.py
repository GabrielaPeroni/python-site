from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone

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
    }
    return render(request, "core/landing.html", context)
