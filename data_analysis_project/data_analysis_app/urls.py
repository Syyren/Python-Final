from django.urls import path
from . import views

#declaring accessible URLs and their paths
urlpatterns = [
    path('', views.index),
    path('titles/',views.view_titles, name='titles'),
    path('get_titles/',views.get_titles_data, name='get_titles_data'),
    path('forg/', views.frog)
]