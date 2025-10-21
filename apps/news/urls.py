from django.urls import path

from . import views

app_name = "news"

urlpatterns = [
    path("", views.news_list_view, name="news_list"),
    path("<slug:slug>/", views.news_detail_view, name="news_detail"),
]
