from django.urls import path
from . import views

#declaring accessible URLs and their paths
urlpatterns = [
path('',views.index),
path('forg/', views.frog),
path('titles/',views.view_titles, name='view_titles'),
]