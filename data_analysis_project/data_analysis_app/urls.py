from django.urls import path
from . import views

#declaring accessible URLs and their paths
urlpatterns = [
    path('', views.index),
    path('titles/',views.view_titles, name='view_titles'),
    path('forg/', views.frog)
]