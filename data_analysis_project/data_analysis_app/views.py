from django.shortcuts import render
from .meme import forg

from django.http import HttpResponse
def frog(request):
    return HttpResponse(forg())