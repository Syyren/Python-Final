from django.urls import path
from . import views

#declaring accessible URLs and their paths
urlpatterns = [
    path('', views.index),
    path('titles/',views.view_titles, name='titles'),
    path('get_titles/',views.get_titles_data, name='get_titles_data'),
    path('analyze/', views.analyze, name = 'analyze'),
    path('genre_graph/', views.genre_graph, name='genre_graph'),
    path('rating_distribution_graph/', views.rating_distribution_graph, name='rating_distribution_graph'),
    path('trend_graph/', views.trend_graph, name='trend_graph'),
    path('top_countries_graph/', views.top_countries_graph, name='top_countries_graph'),
    path('forg/', views.frog)
]