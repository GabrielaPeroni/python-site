from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UserLoginForm, UserRegistrationForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect("core:landing")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, "Cadastro realizado com sucesso! Bem-vindo ao MaricaCity."
            )
            return redirect("core:landing")
    else:
        form = UserRegistrationForm()

    context = {
        "form": form,
        "google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
    }
    return render(request, "accounts/register.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:landing")

    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bem-vindo de volta, {username}!")
                return redirect("core:landing")
    else:
        form = UserLoginForm()

    context = {
        "form": form,
        "google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
    }
    return render(request, "accounts/login.html", context)


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Você saiu com sucesso.")
    return redirect("core:landing")


# Admin User Management Views
@login_required
def user_management_view(request):
    """Admin view to manage all users"""
    if not request.user.can_moderate:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect("core:landing")

    # Get filter parameters
    user_type_filter = request.GET.get("user_type", "")
    status_filter = request.GET.get("status", "")
    search_query = request.GET.get("q", "")

    # Base queryset with statistics
    users = User.objects.annotate(
        places_count=Count("places", distinct=True),
        reviews_count=Count("place_reviews_written", distinct=True),
    ).select_related()

    # Apply filters
    if user_type_filter:
        users = users.filter(user_type=user_type_filter)

    if status_filter == "active":
        users = users.filter(is_active=True)
    elif status_filter == "inactive":
        users = users.filter(is_active=False)

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
        )

    # Get statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    explore_users = User.objects.filter(user_type=User.UserType.EXPLORE).count()
    creation_users = User.objects.filter(user_type=User.UserType.CREATION).count()
    admin_users = User.objects.filter(user_type=User.UserType.ADMIN).count()

    context = {
        "users": users.order_by("-created_at"),
        "total_users": total_users,
        "active_users": active_users,
        "explore_users": explore_users,
        "creation_users": creation_users,
        "admin_users": admin_users,
        "user_type_filter": user_type_filter,
        "status_filter": status_filter,
        "search_query": search_query,
        "user_type_choices": User.UserType.choices,
    }
    return render(request, "accounts/user_management.html", context)


@login_required
def user_update_type_view(request, user_id):
    """Update user type"""
    if not request.user.can_moderate:
        return JsonResponse({"success": False, "error": "Sem permissão"}, status=403)

    if request.method != "POST":
        return JsonResponse(
            {"success": False, "error": "Método não permitido"}, status=405
        )

    user = get_object_or_404(User, id=user_id)
    new_type = request.POST.get("user_type")

    if new_type not in dict(User.UserType.choices):
        return JsonResponse(
            {"success": False, "error": "Tipo de usuário inválido"}, status=400
        )

    # Prevent changing own user type
    if user == request.user:
        return JsonResponse(
            {
                "success": False,
                "error": "Você não pode alterar seu próprio tipo de usuário",
            },
            status=400,
        )

    user.user_type = new_type
    user.save()

    messages.success(
        request,
        f"Tipo de usuário de {user.username} alterado para {user.get_user_type_display()}.",
    )
    return JsonResponse(
        {
            "success": True,
            "message": "Tipo de usuário atualizado",
            "user_type_display": user.get_user_type_display(),
        }
    )


@login_required
def user_toggle_status_view(request, user_id):
    """Toggle user active status"""
    if not request.user.can_moderate:
        return JsonResponse({"success": False, "error": "Sem permissão"}, status=403)

    if request.method != "POST":
        return JsonResponse(
            {"success": False, "error": "Método não permitido"}, status=405
        )

    user = get_object_or_404(User, id=user_id)

    # Prevent deactivating own account
    if user == request.user:
        return JsonResponse(
            {"success": False, "error": "Você não pode desativar sua própria conta"},
            status=400,
        )

    user.is_active = not user.is_active
    user.save()

    status_text = "ativado" if user.is_active else "desativado"
    messages.success(request, f"Usuário {user.username} {status_text} com sucesso.")

    return JsonResponse(
        {
            "success": True,
            "is_active": user.is_active,
            "message": f"Usuário {status_text}",
        }
    )


@login_required
def user_delete_view(request, user_id):
    """Delete user account"""
    if not request.user.can_moderate:
        messages.error(request, "Você não tem permissão para excluir usuários.")
        return redirect("accounts:user_management")

    user = get_object_or_404(User, id=user_id)

    # Prevent deleting own account
    if user == request.user:
        messages.error(request, "Você não pode excluir sua própria conta.")
        return redirect("accounts:user_management")

    if request.method == "POST":
        username = user.username
        user.delete()
        messages.success(request, f"Usuário {username} excluído com sucesso.")
        return redirect("accounts:user_management")

    context = {"user_to_delete": user}
    return render(request, "accounts/user_delete_confirm.html", context)
