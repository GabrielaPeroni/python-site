from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PlaceForm, PlaceImageFormSet, PlaceReviewForm
from .models import Category, Favorite, Place, PlaceApproval, PlaceReview


def explore_view(request):
    """Explore page with categories and all places with search"""

    # Get all active categories with place counts
    categories = Category.objects.filter(is_active=True).order_by("display_order")

    # Get search query
    search_query = request.GET.get("q", "").strip()

    # Get sorting parameter
    sort_by = request.GET.get("sort", "-created_at")
    valid_sorts = {
        "-created_at": "-created_at",
        "name": "name",
        "-name": "-name",
    }
    sort_order = valid_sorts.get(sort_by, "-created_at")

    # Get all approved places with optional search and sorting
    all_places = Place.objects.filter(is_approved=True, is_active=True)

    # Apply search filter if query exists
    if search_query:
        all_places = all_places.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(categories__name__icontains=search_query)
        ).distinct()

    all_places = all_places.prefetch_related("images", "categories").order_by(
        sort_order
    )

    context = {
        "categories": categories,
        "all_places": all_places,
        "current_sort": sort_by,
    }
    return render(request, "explore/explore.html", context)


def category_detail_view(request, slug):
    """Category detail page with all places in the category"""

    # Get the category or 404
    category = get_object_or_404(Category, slug=slug, is_active=True)

    # Get sorting parameter
    sort_by = request.GET.get("sort", "-created_at")
    valid_sorts = {
        "-created_at": "-created_at",
        "name": "name",
        "-name": "-name",
    }
    sort_order = valid_sorts.get(sort_by, "-created_at")

    # Get all approved and active places in this category
    places = (
        Place.objects.filter(categories=category, is_approved=True, is_active=True)
        .prefetch_related("images", "categories", "created_by")
        .order_by(sort_order)
    )

    # Get all categories for navigation
    all_categories = Category.objects.filter(is_active=True).order_by("display_order")

    context = {
        "category": category,
        "places": places,
        "all_categories": all_categories,
        "current_sort": sort_by,
    }
    return render(request, "explore/category_detail.html", context)


def place_detail_view(request, pk):
    """Individual place detail page"""

    # Get the place or 404 (only show approved and active places to non-admin users)
    if request.user.is_authenticated and (
        request.user.user_type == "ADMIN" or request.user.user_type == "CREATION"
    ):
        # Admins and creation users can view their own unapproved places
        place = get_object_or_404(
            Place.objects.prefetch_related("images", "categories"), pk=pk
        )
        # But creation users can only see their own places if unapproved
        if (
            place.created_by != request.user
            and request.user.user_type != "ADMIN"
            and not place.is_approved
        ):
            place = get_object_or_404(Place, pk=pk, is_approved=True, is_active=True)
    else:
        # Regular users can only see approved and active places
        place = get_object_or_404(Place, pk=pk, is_approved=True, is_active=True)

    # Get related places from the same categories
    related_places = (
        Place.objects.filter(
            categories__in=place.categories.all(), is_approved=True, is_active=True
        )
        .exclude(pk=place.pk)
        .distinct()
        .prefetch_related("images", "categories")[:3]
    )

    # Check if user can edit this place
    can_edit = False
    if request.user.is_authenticated:
        if request.user.user_type == "ADMIN" or place.created_by == request.user:
            can_edit = True

    # Get all reviews for this place
    reviews = place.reviews.select_related("user").order_by("-created_at")

    # Check if current user has already reviewed this place
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    # Check if place is favorited by current user
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, place=place).exists()

    # Get favorites count
    favorites_count = place.favorited_by.count()

    context = {
        "place": place,
        "related_places": related_places,
        "can_edit": can_edit,
        "reviews": reviews,
        "user_review": user_review,
        "is_favorited": is_favorited,
        "favorites_count": favorites_count,
    }
    return render(request, "explore/place_detail.html", context)


@login_required
def place_create_view(request):
    """Create a new place (creation-users and admin only)"""

    # Check if user can create places
    if not request.user.can_create_places:
        messages.error(request, "Você não tem permissão para criar lugares.")
        return redirect("explore:explore")

    if request.method == "POST":
        form = PlaceForm(request.POST)
        formset = PlaceImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            # Create the place
            place = form.save(commit=False)
            place.created_by = request.user
            place.is_approved = False  # Always starts as unapproved
            place.save()

            # Save categories (many-to-many relationship)
            form.save_m2m()

            # Save images
            formset.instance = place
            formset.save()

            # Ensure at least one image is marked as primary
            images = place.images.all()
            if images.exists():
                primary_images = images.filter(is_primary=True)
                if not primary_images.exists():
                    # If no primary image is set, make the first one primary
                    first_image = images.first()
                    first_image.is_primary = True
                    first_image.save()
                elif primary_images.count() > 1:
                    # If multiple primary images, keep only the first one
                    primary_images.exclude(id=primary_images.first().id).update(
                        is_primary=False
                    )

            messages.success(
                request,
                f'Lugar "{place.name}" criado com sucesso! Ele será revisado por um administrador antes de aparecer no site.',
            )
            return redirect("explore:place_detail", pk=place.pk)
    else:
        form = PlaceForm()
        formset = PlaceImageFormSet()

    context = {
        "form": form,
        "formset": formset,
        "title": "Adicionar Novo Lugar",
        "submit_text": "Enviar para Aprovação",
    }
    return render(request, "explore/place_form.html", context)


@login_required
def place_update_view(request, pk):
    """Update an existing place (owner or admin only)"""

    # Get the place
    place = get_object_or_404(Place, pk=pk)

    # Check permissions
    if not (request.user.can_moderate or place.created_by == request.user):
        messages.error(request, "Você não tem permissão para editar este lugar.")
        return redirect("explore:place_detail", pk=place.pk)

    if request.method == "POST":
        form = PlaceForm(request.POST, instance=place)
        formset = PlaceImageFormSet(request.POST, request.FILES, instance=place)

        if form.is_valid() and formset.is_valid():
            # Save the place
            updated_place = form.save()

            # Save images
            formset.save()

            # Ensure at least one image is marked as primary
            images = updated_place.images.all()
            if images.exists():
                primary_images = images.filter(is_primary=True)
                if not primary_images.exists():
                    # If no primary image is set, make the first one primary
                    first_image = images.first()
                    first_image.is_primary = True
                    first_image.save()
                elif primary_images.count() > 1:
                    # If multiple primary images, keep only the first one
                    primary_images.exclude(id=primary_images.first().id).update(
                        is_primary=False
                    )

            messages.success(
                request, f'Lugar "{updated_place.name}" atualizado com sucesso!'
            )
            return redirect("explore:place_detail", pk=updated_place.pk)
    else:
        form = PlaceForm(instance=place)
        formset = PlaceImageFormSet(instance=place)

    context = {
        "form": form,
        "formset": formset,
        "place": place,
        "title": f"Editar {place.name}",
        "submit_text": "Salvar Alterações",
    }
    return render(request, "explore/place_form.html", context)


@login_required
def place_delete_view(request, pk):
    """Delete a place (owner or admin only)"""

    place = get_object_or_404(Place, pk=pk)

    # Check permissions
    if not (request.user.can_moderate or place.created_by == request.user):
        messages.error(request, "Você não tem permissão para excluir este lugar.")
        return redirect("explore:place_detail", pk=place.pk)

    if request.method == "POST":
        place_name = place.name
        place.delete()
        messages.success(request, f'Lugar "{place_name}" foi excluído com sucesso.')
        return redirect("explore:explore")

    context = {
        "place": place,
    }
    return render(request, "explore/place_delete_confirm.html", context)


# Admin approval views


@login_required
def approval_queue_view(request):
    """Admin approval queue showing pending places"""

    # Check if user is admin
    if not request.user.can_moderate:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect("explore:explore")

    # Get all pending places (unapproved and active)
    pending_places = (
        Place.objects.filter(is_approved=False, is_active=True)
        .select_related("created_by")
        .prefetch_related("images", "categories")
        .order_by("-created_at")
    )

    context = {
        "pending_places": pending_places,
        "pending_count": pending_places.count(),
    }
    return render(request, "explore/admin/approval_queue.html", context)


@login_required
def approve_place_view(request, pk):
    """Approve a pending place"""

    # Check if user is admin
    if not request.user.can_moderate:
        messages.error(request, "Você não tem permissão para realizar esta ação.")
        return redirect("explore:explore")

    place = get_object_or_404(Place, pk=pk)

    if request.method == "POST":
        # Create approval record
        PlaceApproval.objects.create(
            place=place,
            reviewer=request.user,
            action=PlaceApproval.ActionType.APPROVE,
            comments=request.POST.get("comments", ""),
        )

        messages.success(
            request,
            f'Lugar "{place.name}" foi aprovado com sucesso!',
        )
        return redirect("explore:approval_queue")

    # If GET, redirect to place detail
    return redirect("explore:place_detail", pk=pk)


@login_required
def reject_place_view(request, pk):
    """Reject a pending place"""

    # Check if user is admin
    if not request.user.can_moderate:
        messages.error(request, "Você não tem permissão para realizar esta ação.")
        return redirect("explore:explore")

    place = get_object_or_404(Place, pk=pk)

    if request.method == "POST":
        comments = request.POST.get("comments", "")

        if not comments:
            messages.error(request, "Por favor, forneça um motivo para a rejeição.")
            return redirect("explore:approval_queue")

        # Create rejection record
        PlaceApproval.objects.create(
            place=place,
            reviewer=request.user,
            action=PlaceApproval.ActionType.REJECT,
            comments=comments,
        )

        messages.success(
            request,
            f'Lugar "{place.name}" foi rejeitado.',
        )
        return redirect("explore:approval_queue")

    # If GET, show rejection form
    context = {
        "place": place,
    }
    return render(request, "explore/admin/reject_form.html", context)


@login_required
def backlog_view(request):
    """Admin backlog showing all places with filtering"""

    # Check if user is admin
    if not request.user.can_moderate:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect("explore:explore")

    # Get filter parameters
    status_filter = request.GET.get("status", "all")
    category_filter = request.GET.get("category", "all")
    sort_by = request.GET.get("sort", "-created_at")

    # Start with all places
    places = Place.objects.select_related("created_by").prefetch_related(
        "images", "categories"
    )

    # Apply status filter
    if status_filter == "approved":
        places = places.filter(is_approved=True, is_active=True)
    elif status_filter == "pending":
        places = places.filter(is_approved=False, is_active=True)
    elif status_filter == "rejected":
        places = places.filter(is_active=False)

    # Apply category filter
    if category_filter != "all":
        places = places.filter(categories__slug=category_filter)

    # Apply sorting
    valid_sorts = {
        "-created_at": "-created_at",
        "created_at": "created_at",
        "name": "name",
        "-name": "-name",
    }
    sort_order = valid_sorts.get(sort_by, "-created_at")
    places = places.order_by(sort_order).distinct()

    # Get all categories for filter dropdown
    categories = Category.objects.filter(is_active=True).order_by("name")

    # Get counts for each status
    total_count = Place.objects.count()
    approved_count = Place.objects.filter(is_approved=True, is_active=True).count()
    pending_count = Place.objects.filter(is_approved=False, is_active=True).count()
    rejected_count = Place.objects.filter(is_active=False).count()

    context = {
        "places": places,
        "categories": categories,
        "status_filter": status_filter,
        "category_filter": category_filter,
        "current_sort": sort_by,
        "total_count": total_count,
        "approved_count": approved_count,
        "pending_count": pending_count,
        "rejected_count": rejected_count,
    }
    return render(request, "explore/admin/backlog.html", context)


# Review Views


@login_required
def review_create_view(request, place_pk):
    """Create a new review for a place"""
    place = get_object_or_404(Place, pk=place_pk, is_approved=True, is_active=True)

    # Check if user already reviewed this place
    existing_review = PlaceReview.objects.filter(place=place, user=request.user).first()
    if existing_review:
        messages.warning(
            request, "Você já avaliou este lugar. Edite sua avaliação existente."
        )
        return redirect("explore:place_detail", pk=place.pk)

    if request.method == "POST":
        form = PlaceReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.place = place
            review.user = request.user
            review.save()
            messages.success(request, "Avaliação enviada com sucesso!")
            return redirect("explore:place_detail", pk=place.pk)
    else:
        form = PlaceReviewForm()

    context = {"form": form, "place": place}
    return render(request, "explore/review_form.html", context)


@login_required
def review_edit_view(request, pk):
    """Edit an existing review"""
    review = get_object_or_404(PlaceReview, pk=pk)

    # Check permissions: owner or admin can edit
    if review.user != request.user and request.user.user_type != "ADMIN":
        messages.error(request, "Você não tem permissão para editar esta avaliação.")
        return redirect("explore:place_detail", pk=review.place.pk)

    if request.method == "POST":
        form = PlaceReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Avaliação atualizada com sucesso!")
            return redirect("explore:place_detail", pk=review.place.pk)
    else:
        form = PlaceReviewForm(instance=review)

    context = {"form": form, "place": review.place, "review": review}
    return render(request, "explore/review_form.html", context)


@login_required
def review_delete_view(request, pk):
    """Delete a review"""
    review = get_object_or_404(PlaceReview, pk=pk)

    # Check permissions: owner or admin can delete
    if review.user != request.user and request.user.user_type != "ADMIN":
        messages.error(request, "Você não tem permissão para excluir esta avaliação.")
        return redirect("explore:place_detail", pk=review.place.pk)

    place_pk = review.place.pk
    if request.method == "POST":
        review.delete()
        messages.success(request, "Avaliação excluída com sucesso!")
        return redirect("explore:place_detail", pk=place_pk)

    context = {"review": review}
    return render(request, "explore/review_delete_confirm.html", context)


# Favorite Views


@login_required
def toggle_favorite_view(request, pk):
    """Toggle favorite status for a place (AJAX endpoint)"""
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    place = get_object_or_404(Place, pk=pk, is_approved=True, is_active=True)

    # Check if already favorited
    favorite = Favorite.objects.filter(user=request.user, place=place).first()

    if favorite:
        # Remove favorite
        favorite.delete()
        is_favorited = False
        message = "Lugar removido dos favoritos"
    else:
        # Add favorite
        Favorite.objects.create(user=request.user, place=place)
        is_favorited = True
        message = "Lugar adicionado aos favoritos"

    # Get total favorites count for this place
    favorites_count = place.favorited_by.count()

    return JsonResponse(
        {
            "success": True,
            "is_favorited": is_favorited,
            "favorites_count": favorites_count,
            "message": message,
        }
    )


@login_required
def favorites_list_view(request):
    """List all favorites for the current user"""
    favorites = (
        Favorite.objects.filter(user=request.user)
        .select_related("place", "place__created_by")
        .prefetch_related("place__images", "place__categories")
        .order_by("-created_at")
    )

    context = {
        "favorites": favorites,
        "favorites_count": favorites.count(),
    }
    return render(request, "explore/favorites.html", context)
