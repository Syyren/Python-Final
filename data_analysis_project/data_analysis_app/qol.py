from datetime import datetime
from .models import Title, Director, Cast, ListedIn, TitlesDirectors, TitlesCasts, TitlesListedIns
import pandas as pd

#converts a string like 'a, b, c' to a list like ['a', 'b', 'c']
def str_to_list(string : str):
    list = []
    if string != None:
        list = string.split(",")
        list = [item.strip() for item in list]
    return list

#converts a string formatted in the specified way to a datetime value
def str_to_date(string : str):
    date = None
    if string and string != "nan":
         date = datetime.strptime(string.strip(), "%B %d, %Y").date()
    return date

#pops out the letters from a duration so the number can be worked with
def convert_duration(string : str): 
    list = string.split(" ")
    try:
        if list:
            duration = int(list[0].strip())
    except:
        duration = 0
    return duration

#Helper functions to break up the superfunction of process_data
def fetch_existing_data():
    #pre-fetching related data so I'm not hitting up the db every millisecond during duplicate check
    existing_titles = {title.id for title in Title.objects.all()}
    directors_existing = {director.director_name: director for director in Director.objects.all()}
    casts_existing = {cast.cast_name: cast for cast in Cast.objects.all()}
    listed_ins_existing = {listed_in.listed_in_name: listed_in for listed_in in ListedIn.objects.all()}
    return existing_titles, directors_existing, casts_existing, listed_ins_existing

#inserting titles to db
def process_title(row, existing_titles):
    #checking for duplicates
    if row['show_id'] in existing_titles:
        return None

    #creating title for insert
    return Title(
        id=row['show_id'],
        type=row['type'],
        title=row['title'],
        country=row['country'],
        date_added=str_to_date(str(row['date_added'])),
        release_year=row['release_year'],
        rating=row['rating'],
        duration=convert_duration(str(row['duration'])),
        description=row['description']
    )

#inserting directors and titlesdirectors to db
def process_directors(row, directors_existing, title_obj, directors_to_create : list):
    titles_directors_to_create = []
    if row['director']:
        directors = str(row['director']).split(',')
        for director_name in directors:
            if director_name not in directors_existing:
                director = Director(director_name=director_name.strip())
                directors_existing[director_name] = director
            director = directors_existing[director_name]
            directors_to_create.append(director)
            titles_directors_to_create.append(TitlesDirectors(title=title_obj, director=director))
    return titles_directors_to_create, directors_to_create

#inserting casts and titlescasts to db
def process_casts(row, casts_existing, title_obj, casts_to_create : list):
    titles_casts_to_create = []
    if row['cast']:
        casts = str(row['cast']).split(',')
        for cast_name in casts:
            if cast_name not in casts_existing:
                cast = Cast(cast_name=cast_name.strip())
                casts_existing[cast_name] = cast
            cast = casts_existing[cast_name] 
            casts_to_create.append(cast)     
            titles_casts_to_create.append(TitlesCasts(title=title_obj, cast=cast))
    return titles_casts_to_create, casts_to_create

#inserting listed_ins and titleslistedins to db
def process_listed_ins(row, listed_ins_existing, title_obj, listed_ins_to_create : list):
    titles_listedins_to_create = []
    if row['listed_in']:
        listed_ins = str(row['listed_in']).split(',')
        for listed_in_name in listed_ins:
            if listed_in_name not in listed_ins_existing:
                listed_in = ListedIn(listed_in_name=listed_in_name.strip())
                listed_ins_existing[listed_in_name] = listed_in
            listed_in = listed_ins_existing[listed_in_name]
            listed_ins_to_create.append(listed_in)
            titles_listedins_to_create.append(TitlesListedIns(title=title_obj, listed_in=listed_in))
    return titles_listedins_to_create, listed_ins_to_create


#Taking the csv and converting it into the db
def process_data():
    df = pd.read_csv("data_analysis_app/netflix_titles.csv")

    #getting existing data from database
    existing_titles, directors_existing, casts_existing, listed_ins_existing = fetch_existing_data()

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

        #saving primary Titles table
        title_obj = process_title(row, existing_titles)
        if not title_obj:
            continue  # Skip duplicate titles
        titles_to_create.append(title_obj)

        #saving secondary tables and intermediary table connections
        tdtc, directors_to_create = process_directors(row, directors_existing, title_obj, directors_to_create)
        tctc, casts_to_create = process_casts(row, casts_existing, title_obj, casts_to_create)
        tltc, listed_ins_to_create = process_listed_ins(row, listed_ins_existing, title_obj, listed_ins_to_create)
        titles_directors_to_create.extend(tdtc)
        titles_casts_to_create.extend(tctc)
        titles_listedins_to_create.extend(tltc)

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