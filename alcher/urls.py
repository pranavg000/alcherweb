"""alcher URL Configurationi

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
urlpatterns = [
    path('',RedirectView.as_view(url  ='/auths/login/')),
    path('admin/', admin.site.urls),
    path('auths/', include('auths.urls', namespace='auths')),
    path('caportal/', include('ca.urls', namespace='ca')),
    path("fbshare/",include("fbshare.urls",namespace="fb")),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(template_name="auths/password_reset_form.html"), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name="auths/password_reset_done.html"), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name="auths/password_reset_confirm.html"), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(template_name="auths/password_reset_complete.html"), name='password_reset_complete'),
]

#urlpatterns+= static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
