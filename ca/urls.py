from django.urls import path
from . import views

app_name = 'ca'

urlpatterns = [
    path('home', views.home, name='home'),
    path('contact', views.contactUs , name='contactUs'),
    path('faqs', views.faqs , name='faqs'),
    path('venue', views.venue , name='venue'),
    path('questionnaire', views.questionnare, name='questionnare'),
    path('pending', views.pending, name='pending'),
    path('guidelines', views.guidelines, name='guidelines'),
    path('hospitality', views.hospitality, name='hospitality'),
    path('poc', views.poc, name='poc'),
    path('submitideas', views.submitIdea, name='submitIdea'),
    path('standings', views.standings, name='standings'),
    path('notifications', views.notifications, name='notifications')
]
