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
        self.director : list = str_to_list(str(director))
        self.cast : list = str_to_list(str(cast))
        self.country : list = str_to_list(str(country))
        self.date_added : date = str_to_date(str(date_added))
        self.release_year : int = release_year
        self.rating : str = rating
        self.duration : int = convert_duration(str(duration))
        self.listed_in : list = str_to_list(str(listed_in))
        self.description : str = description

    def getDurationAsString(self):
        duration_string = f"{self.duration}"
        s = ""
        if self.duration > 1:
            s = "s"
        if self.type == "Movie":
            duration_string += f" min{s}"
        elif self.type == "TV Show":
            duration_string += f" Season{s}"
        return duration_string