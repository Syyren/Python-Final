from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from django.utils.safestring import mark_safe

from .qol import process_data
from .meme import forg
from .models import Title

def index(request):
    return render(request, "index.html")

def frog(request):
    return render(request, "forg.html", {"forg" : mark_safe(forg())})

@never_cache
def get_titles_data(request):
    #processing csv
    process_data()
    #db query for titles
    #prefetching relational data
    titles = Title.objects.prefetch_related('directors', 'casts', 'listed_in').all()
    data = []
    for title in titles:
        data.append({
            'type': title.type,
            'title': title.title,
            'directors': [director.director_name for director in title.directors.all()],
            'casts': [cast.cast_name for cast in title.casts.all()],
            'country': title.country,
            'date_added': title.date_added,
            'release_year': title.release_year,
            'rating': title.rating,
            'duration': title.duration,
            'listed_in': [category.listed_in_name for category in title.listed_in.all()],
            'description': title.description,
            })
    
    #disable caching - remove after developemnt
    response = JsonResponse({'titles': data})
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response
    
def view_titles(request):
    return render(request, "view_titles.html")