from django.urls import path
from . import views as auths_views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.conf.urls import url,include



app_name = 'auths'

urlpatterns = [
    path('register/', auths_views.register, name="register"),
    path('home/', TemplateView.as_view(template_name="auths/home.html"), name="home"),
    path('login/', auths_views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="auths/logout.html"), name='logout'),
    path('social-auth/', include('social_django.urls', namespace="social")),
    url(r'^account_activation_sent/$', auths_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    	auths_views.activate, name='activate'),
    
]
