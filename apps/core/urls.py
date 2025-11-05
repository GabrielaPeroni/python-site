from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.landing_view, name="landing"),
    path("sobre/", views.about_view, name="about"),
    path("painel-admin/", views.admin_dashboard_view, name="admin_dashboard"),
    path("painel-admin/noticias/", views.admin_news_list_view, name="admin_news_list"),
    path(
        "painel-admin/noticias/criar/",
        views.admin_news_create_view,
        name="admin_news_create",
    ),
    path(
        "painel-admin/noticias/<int:pk>/editar/",
        views.admin_news_edit_view,
        name="admin_news_edit",
    ),
    path(
        "painel-admin/noticias/<int:pk>/excluir/",
        views.admin_news_delete_view,
        name="admin_news_delete",
    ),
]
