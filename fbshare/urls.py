from django.urls import path 
from .views import *

app_name = "fb"
urlpatterns = [
        path("fb/",view=fb),
        path("invite/" ,view = invite_all,name ="invite_all")
        ]


