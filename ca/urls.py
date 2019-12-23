from django.urls import path
from . import views

app_name = 'ca'

urlpatterns = [
    path('contact', views.contactUs , name='contactUs'),
    path('faqs', views.faqs , name='faqs'),
    path('venue', views.venue , name='venue'),
    path('questionnare', views.questionnare, name='questionnare'),
]
