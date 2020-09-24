from django.shortcuts import render
from .fbshare import *
from django.http import HttpResponse
# Create your views here.


def fb(request) :
    get_page_posts()
    get_user_posts() 

    return HttpResponse("run successful") 



