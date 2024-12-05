from django.shortcuts import render
from django.utils.safestring import mark_safe
from .meme import forg
from .models import Title, Director, Cast, ListedIn, TitlesDirectors, TitlesCasts, TitlesListedIns
import pandas as pd

df = pd.read_csv("data_analysis_app/netflix_titles.csv")

#Saving Title and relational data
for _, row in df.iterrows():
    
    #saving primary Titles table
    title_obj = Title.objects.create(
        id=row['show_id'],
        type=row['type'],
        title=row['title'],
        country=row['country'],
        date_added=row['date_added'],
        release_year=row['release_year'],
        rating=row['rating'],
        duration=row['duration'],
        description=row['description']
    )


    #saving secondary tables and intermediary table connections
    if row['director']:
        directors = row['director'].split(',')
        for director_name in directors:
            #Stops duplicates
            director, _ = Director.objects.get_or_create(director_name=director_name.strip())
            #creating relationship in TitlesDirectors
            TitlesDirectors.objects.create(title=title_obj, director=director)

    if row['cast']:
        casts = row['cast'].split(',')
        for cast_name in casts:
            #Stops duplicates
            cast, _ = Cast.objects.get_or_create(cast_name=cast_name.strip())
            #creating relationship in TitlesCasts
            TitlesCasts.objects.create(title=title_obj, cast=cast)
    
    if row['listed_in']:
        listed_ins = row['listed_in'].split(',')
        for listed_in_name in listed_ins:
            #Stops duplicates
            listed_in, _ = ListedIn.objects.get_or_create(listed_in_name=listed_in_name.strip())
            #creating relationship in TitlesListedIns
            TitlesListedIns.objects.create(title=title_obj, listed_in=listed_in)


def index(request):
    return render(request, "index.html")

def frog(request):
    return render(request, "forg.html", {"forg" : mark_safe(forg())})

def view_titles(request):
    #db query for titles
    titles = Title.objects.all()
    return render(request, "view_title.html", {"titles":titles})