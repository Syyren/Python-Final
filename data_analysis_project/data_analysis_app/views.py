from django.http import JsonResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe

from .qol import process_data
from .meme import forg
from .models import Title

def index(request):
    return render(request, "index.html")

def frog(request):
    return render(request, "forg.html", {"forg" : mark_safe(forg())})


def get_titles_data(request):
    #processing csv
    process_data()
    #db query for titles
    #prefetching relational data
    titles = Title.objects.prefetch_related('directors', 'casts', 'listed_in').all()
    data = []
    for title in titles:
        data.append({
            'title': title.title,
            'type': title.type,
            'release_year': title.release_year,
            'rating': title.rating,
            'directors': [director.director_name for director in title.directors.all()],
            'casts': [cast.cast_name for cast in title.casts.all()],
            'listed_in': [category.listed_in_name for category in title.listed_in.all()],
            'description': title.description,
            })
    return JsonResponse({'titles': data})
    
def view_titles(request):
    return render(request, "view_titles.html")