from django.shortcuts import render
from django.utils.safestring import mark_safe
from .meme import forg
from .models import Title, Director, Cast, ListedIn, TitlesDirectors, TitlesCasts, TitlesListedIns
import pandas as pd

df = pd.read_csv("data_analysis_app/netflix_titles.csv")

#pre-fetching related data so I'm not hitting up the db every millisecond during duplicate check
existing_titles = {title.id for title in Title.objects.all()}
directors_existing = {director.director_name: director for director in Director.objects.all()}
casts_existing = {cast.cast_name: cast for cast in Cast.objects.all()}
listed_ins_existing = {listed_in.listed_in_name: listed_in for listed_in in ListedIn.objects.all()}

# making lists for bulk create so we're not saving to the db every row
titles_to_create = []
directors_to_create = []
casts_to_create = []
listed_ins_to_create = []
titles_directors_to_create = []
titles_casts_to_create = []
titles_listedins_to_create = []

#Saving Title and relational data
for _, row in df.iterrows():
    #stopping duplicate titles
    if row['show_id'] in existing_titles:
        continue

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
    titles_to_create.append(title_obj)

    #saving secondary tables and intermediary table connections
    if row['director']:
        directors = row['director'].split(',')
        for director_name in directors:
            #Stops duplicates
            if director_name not in directors_existing:
                director = Director(director_name=director_name.strip())
                #adding to bulk list
                directors_to_create.append(director)
                directors_existing[director_name] = director
            director = directors_existing[director_name]
            #creating relationship in TitlesDirectors
            titles_directors_to_create.append(TitlesDirectors(title=title_obj, director=director))

    if row['cast']:
        casts = row['cast'].split(',')
        for cast_name in casts:
            #Stops duplicates
            if cast_name not in casts_existing:
                cast = Cast(cast_name=cast_name.strip())
                #adding to bulk list
                casts_to_create.append(cast)
                casts_existing[cast_name] = cast
            cast = casts_existing[cast_name]      
            #creating relationship in TitlesCasts
            titles_casts_to_create.append(TitlesCasts(title=title_obj, cast=cast))
    
    if row['listed_in']:
        listed_ins = row['listed_in'].split(',')
        for listed_in_name in listed_ins:
            #Stops duplicates
            if listed_in_name not in listed_ins_existing:
                listed_in = ListedIn(listed_in_name=listed_in_name.strip())
                #adding to bulk list
                listed_ins_to_create.append(listed_in)
                listed_ins_existing[listed_in_name] = listed_in
            listed_in = listed_ins_existing[listed_in_name]
            #creating relationship in TitlesListedIns
            titles_listedins_to_create.append(TitlesListedIns(title=title_obj, listed_in=listed_in))

#bulk create Primary table
if titles_to_create:
    Title.objects.bulk_create(titles_to_create)
#bulk create secondary tables
if directors_to_create:
    Director.objects.bulk_create(directors_to_create)
if casts_to_create:
    Cast.objects.bulk_create(casts_to_create)
if listed_ins_to_create:
    ListedIn.objects.bulk_create(listed_ins_to_create)
#bulk create intermediary tables
if titles_directors_to_create:
    TitlesDirectors.objects.bulk_create(titles_directors_to_create)
if titles_casts_to_create:
    TitlesCasts.objects.bulk_create(titles_casts_to_create)
if titles_listedins_to_create:
    TitlesListedIns.objects.bulk_create(titles_listedins_to_create)



def index(request):
    return render(request, "index.html")

def frog(request):
    return render(request, "forg.html", {"forg" : mark_safe(forg())})

def view_titles(request):
    #db query for titles
                           #prefetching relational data
    titles = Title.objects.prefetch_related('directors', 'casts', 'listed_in').all()
    return render(request, "view_title.html", {"titles":titles})