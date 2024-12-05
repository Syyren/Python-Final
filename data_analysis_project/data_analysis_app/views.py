from django.shortcuts import render
from django.utils.safestring import mark_safe
from .meme import forg
from .models import Title
import pandas as pd

df = pd.read_csv("data_analysis_app/netflix_titles.csv")

titles = []

for _, row in df.iterrows():
    title_obj = Title(
        id=row['show_id'],
        type=row['type'],
        title=row['title'],
        director=row['director'],
        cast=row['cast'],
        country=row['country'],
        date_added=row['date_added'],
        release_year=row['release_year'],
        rating=row['rating'],
        duration=row['duration'],
        listed_in=row['listed_in'],
        description=row['description']
    )
    titles.append(title_obj)

print(titles[1].title)

def index(request):
    return render(request, "index.html")

def frog(request):
    return render(request, "forg.html", {"forg" : mark_safe(forg())})

def view_titles(request):
    return render(request, "view_title.html", {"titles":titles})
