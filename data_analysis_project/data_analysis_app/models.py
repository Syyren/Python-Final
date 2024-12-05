from django.db import models
from datetime import date
from .qol import str_to_list, str_to_date, convert_duration

class Title():
    def __init__(self, id : str,
                 type : str,
                 title : str, 
                 director: str,
                 cast: str,
                 country: str,
                 date_added : str,
                 release_year: int,
                 rating: str,
                 duration: str,
                 listed_in: list,
                 description: str):
        self.__id : str = id
        self.type = type
        self.title : str = title
        self.director : list = str_to_list(director)
        self.cast : list = str_to_list(cast)
        self.country : list = str_to_list(country)
        self.date_added : date = str_to_date(date_added)
        self.release_year : int = release_year
        self.rating : str = rating
        self.duration : int = convert_duration(duration)
        self.listed_in : list = str_to_list(listed_in)
        self.description : str = description