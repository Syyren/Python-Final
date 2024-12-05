from django.shortcuts import render
from django.utils.safestring import mark_safe
from .meme import forg

from django.http import HttpResponse

def frog(request):
    return render(request, "forg.html", {"name" : "Steven", "forg" : mark_safe(forg())})

