from django.shortcuts import render
from django.utils.safestring import mark_safe
import pandas as pd

from .qol import process_data
from .meme import forg
from .models import Title

def index(request):
    return render(request, "index.html")

def frog(request):
    return render(request, "forg.html", {"forg" : mark_safe(forg())})

def view_titles(request):
    #run the csv processing
    process_data()
    #db query for titles
    #prefetching relational data
    titles = Title.objects.prefetch_related('directors', 'casts', 'listed_in').all()
    return render(request, "view_titles.html", {"titles":titles})