"""owasp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import login,logout,create_user_view,test,home
import django.views.defaults

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/',login,name='login'),
    url(r'^$',home,name='home'),
    url(r'^logout/$',logout,name='logout'),
    url(r'^storage/', include('base.urls',namespace='base_app')),
    url(r'^404/$', django.views.defaults.page_not_found, ),

    url(r'^register/',create_user_view,name='register'),
    url(r'^test/',test,name='test'),
    url(r'^PageNotFoundError/',test,name='error'),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)