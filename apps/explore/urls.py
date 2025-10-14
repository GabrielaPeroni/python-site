from django.urls import path
from . import views

app_name = 'explore'

urlpatterns = [
    path('', views.explore_view, name='explore'),
    path('category/<slug:slug>/', views.category_detail_view, name='category_detail'),
    path('place/<int:pk>/', views.place_detail_view, name='place_detail'),
]
