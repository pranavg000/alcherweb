from django.urls import path 
from .views import *

app_name = "fbshare"
urlpatterns = [
        path("fb/",view=fb),
        ]


