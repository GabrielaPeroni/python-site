from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import UserLoginForm, UserRegistrationForm


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
