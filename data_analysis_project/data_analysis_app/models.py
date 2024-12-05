from django.db import models

class Title(models.Model):
    id = models.CharField(max_length=10, primary_key=True) #good to show_id: s999999999
    type = models.CharField(max_length=50)
    title = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    date_added = models.DateField(blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    rating = models.CharField(max_length=10, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

class Director(models.Model):
    id = models.AutoField(primary_key=True)
    director_name = models.CharField(max_length=255)

class Cast(models.Model):
    id = models.AutoField(primary_key=True)
    cast_name = models.CharField(max_length=255)

class ListedIn(models.Model):
    id = models.AutoField(primary_key=True)
    listed_in_name = models.CharField(max_length=255)

class TitleDirector(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)

class TitleCast(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    cast = models.ForeignKey(Cast, on_delete=models.CASCADE)

class TitleListedIn(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    listed_in = models.ForeignKey(ListedIn, on_delete=models.CASCADE)
