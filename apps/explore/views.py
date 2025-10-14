from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Place, Category, PlaceImage
from .forms import PlaceForm, PlaceImageFormSet


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


@login_required
def place_create_view(request):
    """Create a new place (creation-users and admin only)"""
    
    # Check if user can create places
    if not request.user.can_create_places:
        messages.error(request, 'Você não tem permissão para criar lugares.')
        return redirect('explore:explore')
    
    if request.method == 'POST':
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
                    primary_images.exclude(id=primary_images.first().id).update(is_primary=False)
            
            messages.success(
                request, 
                f'Lugar "{place.name}" criado com sucesso! Ele será revisado por um administrador antes de aparecer no site.'
            )
            return redirect('explore:place_detail', pk=place.pk)
    else:
        form = PlaceForm()
        formset = PlaceImageFormSet()
    
    context = {
        'form': form,
        'formset': formset,
        'title': 'Adicionar Novo Lugar',
        'submit_text': 'Enviar para Aprovação',
    }
    return render(request, 'explore/place_form.html', context)


@login_required 
def place_update_view(request, pk):
    """Update an existing place (owner or admin only)"""
    
    # Get the place
    place = get_object_or_404(Place, pk=pk)
    
    # Check permissions
    if not (request.user.can_moderate or place.created_by == request.user):
        messages.error(request, 'Você não tem permissão para editar este lugar.')
        return redirect('explore:place_detail', pk=place.pk)
    
    if request.method == 'POST':
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
                    primary_images.exclude(id=primary_images.first().id).update(is_primary=False)
            
            messages.success(request, f'Lugar "{updated_place.name}" atualizado com sucesso!')
            return redirect('explore:place_detail', pk=updated_place.pk)
    else:
        form = PlaceForm(instance=place)
        formset = PlaceImageFormSet(instance=place)
    
    context = {
        'form': form,
        'formset': formset,
        'place': place,
        'title': f'Editar {place.name}',
        'submit_text': 'Salvar Alterações',
    }
    return render(request, 'explore/place_form.html', context)


@login_required
def place_delete_view(request, pk):
    """Delete a place (owner or admin only)"""
    
    place = get_object_or_404(Place, pk=pk)
    
    # Check permissions
    if not (request.user.can_moderate or place.created_by == request.user):
        messages.error(request, 'Você não tem permissão para excluir este lugar.')
        return redirect('explore:place_detail', pk=place.pk)
    
    if request.method == 'POST':
        place_name = place.name
        place.delete()
        messages.success(request, f'Lugar "{place_name}" foi excluído com sucesso.')
        return redirect('explore:explore')
    
    context = {
        'place': place,
    }
    return render(request, 'explore/place_delete_confirm.html', context)
