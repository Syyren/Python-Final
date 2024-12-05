import datetime

def str_to_list(string : str):
    list = []
    if string != None:
        list = string.split(",")
        list = [item.strip() for item in list]
    return list

def str_to_date(string : str):
    date = None
    if string:
         date = datetime.strptime(string, "%B %d, %Y").date()
    return date

def convert_duration(string : str):
    duration = 0
    list = string.split(" ")
    if list:
        duration = int(list[0])
    return duration