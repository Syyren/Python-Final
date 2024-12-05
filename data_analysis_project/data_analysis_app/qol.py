from datetime import datetime

def str_to_list(string : str):
    list = []
    if string != None:
        list = string.split(",")
        list = [item.strip() for item in list]
    return list

def str_to_date(string : str):
    date = None
    if string and string != "nan":
         date = datetime.strptime(string.strip(), "%B %d, %Y").date()
    return date

def convert_duration(string : str): 
    list = string.split(" ")
    try:
        if list:
            duration = int(list[0].strip())
    except:
        duration = 0
    return duration