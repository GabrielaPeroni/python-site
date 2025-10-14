from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Place, Category


def explore_view(request):
    """Explore page with categories, newly added, and trending places"""

    # Get all active categories with place counts
    categories = Category.objects.filter(is_active=True).order_by('display_order')

    # Get newly added places (approved in last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    newly_added = Place.objects.filter(
        is_approved=True,
        is_active=True,
        created_at__gte=seven_days_ago
    ).prefetch_related('images', 'categories').order_by('-created_at')[:6]

    # Get trending/spotlight places (most recent if no view tracking)
    trending_places = Place.objects.filter(
        is_approved=True,
        is_active=True
    ).prefetch_related('images', 'categories').order_by('-created_at')[:6]

    # Get sorting parameter
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = {
        '-created_at': '-created_at',
        'name': 'name',
        '-name': '-name',
    }
    sort_order = valid_sorts.get(sort_by, '-created_at')

    # Get all approved places with sorting
    all_places = Place.objects.filter(
        is_approved=True,
        is_active=True
    ).prefetch_related('images', 'categories').order_by(sort_order)

    context = {
        'categories': categories,
        'newly_added': newly_added,
        'trending_places': trending_places,
        'all_places': all_places,
        'current_sort': sort_by,
    }
    return render(request, 'explore/explore.html', context)


def category_detail_view(request, slug):
    """Category detail page with all places in the category"""

    # Get the category or 404
    category = get_object_or_404(Category, slug=slug, is_active=True)

    # Get sorting parameter
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = {
        '-created_at': '-created_at',
        'name': 'name',
        '-name': '-name',
    }
    sort_order = valid_sorts.get(sort_by, '-created_at')

    # Get all approved and active places in this category
    places = Place.objects.filter(
        categories=category,
        is_approved=True,
        is_active=True
    ).prefetch_related('images', 'categories', 'created_by').order_by(sort_order)

    # Get all categories for navigation
    all_categories = Category.objects.filter(is_active=True).order_by('display_order')

    context = {
        'category': category,
        'places': places,
        'all_categories': all_categories,
        'current_sort': sort_by,
    }
    return render(request, 'explore/category_detail.html', context)


def place_detail_view(request, pk):
    """Individual place detail page"""

    # Get the place or 404 (only show approved and active places to non-admin users)
    if request.user.is_authenticated and (request.user.user_type == 'ADMIN' or request.user.user_type == 'CREATION'):
        # Admins and creation users can view their own unapproved places
        place = get_object_or_404(Place.objects.prefetch_related('images', 'categories'), pk=pk)
        # But creation users can only see their own places if unapproved
        if place.created_by != request.user and request.user.user_type != 'ADMIN' and not place.is_approved:
            place = get_object_or_404(Place, pk=pk, is_approved=True, is_active=True)
    else:
        # Regular users can only see approved and active places
        place = get_object_or_404(Place, pk=pk, is_approved=True, is_active=True)

    # Get related places from the same categories
    related_places = Place.objects.filter(
        categories__in=place.categories.all(),
        is_approved=True,
        is_active=True
    ).exclude(pk=place.pk).distinct().prefetch_related('images', 'categories')[:3]

    # Check if user can edit this place
    can_edit = False
    if request.user.is_authenticated:
        if request.user.user_type == 'ADMIN' or place.created_by == request.user:
            can_edit = True

    context = {
        'place': place,
        'related_places': related_places,
        'can_edit': can_edit,
    }
    return render(request, 'explore/place_detail.html', context)
