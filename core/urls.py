# Dentro de core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('filme/<int:filme_id>/', views.filme_detalhe_view, name='filme_detalhe'),
    path('serie/<int:serie_id>/', views.serie_detalhe_view, name='serie_detalhe'),
    path('artista/<int:artista_id>/', views.artista_detalhe_view, name='artista_detalhe'),
    path('episodio/<int:episodio_id>/', views.episodio_detalhe_view, name='episodio_detalhe'),
]