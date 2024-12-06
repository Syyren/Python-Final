import matplotlib.pyplot as plt
#changing matplotlib to use "Off Screen Rendering" or something because errors otherwise
import matplotlib
matplotlib.use('Agg')
import io

from django.http import HttpResponse
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
        duration = ""
        if title.type == "Movie":
            duration = f"{title.duration} Mins"
        if title.type == "TV Show":
            s = ""
            if title.duration > 1:
                s = "s"
            duration = f"{title.duration} Season{s}"
        data.append({
            'type': title.type,
            'title': title.title,
            'directors': [director.director_name for director in title.directors.all()],
            'casts': [cast.cast_name for cast in title.casts.all()],
            'country': title.country,
            'date_added': title.date_added,
            'release_year': title.release_year,
            'rating': title.rating,
            'duration': duration,
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

def analyze(request):
    return render(request, "analyze.html")

def top_countries_graph(request):
    #clearing graph then querying data
    plt.clf()
    titles = Title.objects.all()
    countries = [title.country for title in titles if title.country and title.country != 'nan']

    #grabbing top 10
    country_counts = {country: countries.count(country) for country in set(countries)}
    sorted_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    country_labels, country_values = zip(*sorted_countries)

    #creating graph
    plt.figure(figsize=(8, 6))
    plt.bar(country_labels, country_values, color='coral')
    plt.title('Top 10 Countries with Most Content')
    plt.xlabel('Country')
    plt.ylabel('Number of Titles')
    plt.xticks(rotation=45)
    plt.tight_layout()

    #creating png for rendering to template
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return HttpResponse(buffer, content_type='image/png')

def genre_graph(request):
    #clearing graph then querying data
    plt.clf()
    titles = Title.objects.prefetch_related('listed_in').all()
    genres = []

    for title in titles:
        for genre in title.listed_in.all():
            genres.append(genre.listed_in_name)
    
    #grabbing top 10
    genre_counts = {genre: genres.count(genre) for genre in set(genres)}
    sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
    genre_labels, genre_values = zip(*sorted_genres[:10])

    #creating graph
    plt.figure(figsize=(8, 6))
    plt.bar(genre_labels, genre_values, color='skyblue')
    plt.title('Top 10 Genres on Netflix')
    plt.xlabel('Genres')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    #creating png for use in template
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return HttpResponse(buffer, content_type='image/png')

def rating_distribution_graph(request):
    #clearing graph then querying data
    plt.clf()
    titles = Title.objects.all()
    ratings = [title.rating for title in titles if title.rating]

    #grabbing ratings data
    rating_counts = {rating: ratings.count(rating) for rating in set(ratings)}
    sorted_ratings = sorted(rating_counts.items(), key=lambda x: x[0])
    rating_labels, rating_values = zip(*sorted_ratings)

    #creating graph
    plt.figure(figsize=(8, 6))
    plt.bar(rating_labels, rating_values, color='lightgreen')
    plt.title('Content Distribution by Ratings')
    plt.xlabel('Ratings')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Frequency')
    plt.tight_layout()

    #creating png of graph for template display
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return HttpResponse(buffer, content_type='image/png')

def trend_graph(request):
    #clearing graph then querying data
    plt.clf()
    titles = Title.objects.all()
    additions = [title.date_added.year for title in titles if title.date_added]

    #grabbing yearly additions data
    addition_counts = {year: additions.count(year) for year in set(additions)}
    sorted_additions = sorted(addition_counts.items())  # Sort by year
    years, counts = zip(*sorted_additions)

    #creating graphs
    plt.figure(figsize=(10, 6))
    plt.plot(years, counts, marker='o', linestyle='-', color='purple')
    plt.title('Trend of Additions Over the Years')
    plt.xlabel('Year')
    plt.ylabel('Number of Additions')
    plt.grid(True)
    plt.tight_layout()

    #creating png of graph for template display
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return HttpResponse(buffer, content_type='image/png')
