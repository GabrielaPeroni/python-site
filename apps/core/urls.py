from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.landing_view, name="landing"),
    path("sobre/", views.about_view, name="about"),
    path("painel-admin/", views.admin_dashboard_view, name="admin_dashboard"),
]
