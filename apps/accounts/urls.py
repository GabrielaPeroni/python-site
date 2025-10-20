from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # User Management
    path("usuarios/", views.user_management_view, name="user_management"),
    path(
        "usuarios/<int:user_id>/tipo/",
        views.user_update_type_view,
        name="user_update_type",
    ),
    path(
        "usuarios/<int:user_id>/status/",
        views.user_toggle_status_view,
        name="user_toggle_status",
    ),
    path(
        "usuarios/<int:user_id>/excluir/",
        views.user_delete_view,
        name="user_delete",
    ),
]
