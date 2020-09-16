from django.urls import path, re_path
from . import views as auths_views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.conf.urls import include



app_name = 'auths'

urlpatterns = [
    path('register/', auths_views.register, name="register"),
    path('home/', TemplateView.as_view(template_name="auths/home.html"), name="home"),
    path('login/', auths_views.login, name='login'),
    path('verifymail/', auths_views.verifyEmail, name='verifyEmail'),
    path('logout/', auths_views.logout_, name='logout'),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('register_oauth/', auths_views.register_oauth, name="register_oauth"),
    path('account_activation_sent/', auths_views.account_activation_sent, name='account_activation_sent'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
    	auths_views.activate, name='activate'),
    path('resendmail/' , auths_views.resendMail, name='resendMail'),
    
]
