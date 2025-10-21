from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import News, NewsCategory


def news_list_view(request):
    """Display list of all published news and events"""
    # Get filter parameters
    category_filter = request.GET.get("category", "all")
    sort_by = request.GET.get("sort", "newest")

    # Base query - only published items with publish_date <= now
    news_items = News.objects.filter(
        status=News.PUBLISHED, publish_date__lte=timezone.now()
    )

    # Filter by category if specified
    if category_filter != "all":
        news_items = news_items.filter(category__name=category_filter)

    # Sort
    if sort_by == "oldest":
        news_items = news_items.order_by("publish_date")
    elif sort_by == "popular":
        news_items = news_items.order_by("-view_count", "-publish_date")
    else:  # newest (default)
        news_items = news_items.order_by("-publish_date")

    # Get categories for filter menu
    categories = NewsCategory.objects.all()

    # Separate upcoming events
    upcoming_events = news_items.filter(
        category__name=NewsCategory.EVENT, event_date__gt=timezone.now()
    ).order_by("event_date")[:3]

    # Get featured items
    featured_items = news_items.filter(is_featured=True)[:3]

    context = {
        "news_items": news_items,
        "categories": categories,
        "current_category": category_filter,
        "current_sort": sort_by,
        "upcoming_events": upcoming_events,
        "featured_items": featured_items,
    }

    return render(request, "news/news_list.html", context)


def news_detail_view(request, slug):
    """Display detail page for a single news/event item"""
    news_item = get_object_or_404(
        News, slug=slug, status=News.PUBLISHED, publish_date__lte=timezone.now()
    )

    # Increment view count
    news_item.increment_view_count()

    # Get related news (same category, exclude current)
    related_news = (
        News.objects.filter(
            category=news_item.category,
            status=News.PUBLISHED,
            publish_date__lte=timezone.now(),
        )
        .exclude(id=news_item.id)
        .order_by("-publish_date")[:3]
    )

    context = {
        "news_item": news_item,
        "related_news": related_news,
    }

    return render(request, "news/news_detail.html", context)
