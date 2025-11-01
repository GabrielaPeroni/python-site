"""
API views for the explore app
Provides JSON endpoints for map integration and other features
"""

from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Place


@require_GET
def map_data_api(request):
    """
    API endpoint that returns all approved places with coordinates in JSON format
    Used by the landing page interactive map
    """
    # Get all approved places with coordinates
    places = (
        Place.objects.filter(
            is_approved=True,
            is_active=True,
            latitude__isnull=False,
            longitude__isnull=False,
        )
        .prefetch_related("images", "categories")
        .order_by("-created_at")
    )

    # Build response data
    places_data = []
    for place in places:
        # Get primary image or first image
        primary_image = place.primary_image
        image_url = primary_image.image.url if primary_image else None

        # Get first category for icon/color
        first_category = place.categories.first()
        category_name = first_category.name if first_category else "Outros"
        category_icon = first_category.icon if first_category else "📍"

        places_data.append(
            {
                "id": place.id,
                "name": place.name,
                "description": (
                    place.description[:100] + "..."
                    if len(place.description) > 100
                    else place.description
                ),
                "latitude": float(place.latitude),
                "longitude": float(place.longitude),
                "image_url": image_url,
                "category": category_name,
                "category_icon": category_icon,
                "url": f"/explorar/{place.id}/",
                "rating": float(place.average_rating) if place.average_rating else None,
                "review_count": place.reviews.count(),
            }
        )

    return JsonResponse({"places": places_data, "count": len(places_data)})


@require_GET
def places_by_ids_api(request):
    """
    API endpoint that returns place details for given IDs
    Used by favorites page for anonymous users
    """
    # Get comma-separated IDs from query parameter
    ids_param = request.GET.get("ids", "")

    if not ids_param:
        return JsonResponse({"places": [], "count": 0})

    # Parse IDs
    try:
        place_ids = [int(id.strip()) for id in ids_param.split(",") if id.strip()]
    except ValueError:
        return JsonResponse({"error": "Invalid ID format"}, status=400)

    # Get places
    places = (
        Place.objects.filter(
            id__in=place_ids,
            is_approved=True,
            is_active=True,
        )
        .prefetch_related("images", "categories", "created_by")
        .order_by("-created_at")
    )

    # Build response data
    places_data = []
    for place in places:
        # Get primary image or first image
        primary_image = place.primary_image
        image_url = primary_image.image.url if primary_image else None

        # Get categories
        categories = [
            {
                "name": cat.name,
                "icon": cat.icon if cat.icon else "",
                "slug": cat.slug,
            }
            for cat in place.categories.all()
        ]

        places_data.append(
            {
                "id": place.id,
                "name": place.name,
                "description": place.description,
                "image_url": image_url,
                "categories": categories,
                "url": f"/explorar/place/{place.id}/",
                "rating": float(place.average_rating) if place.average_rating else None,
                "review_count": place.reviews.count(),
            }
        )

    return JsonResponse({"places": places_data, "count": len(places_data)})
