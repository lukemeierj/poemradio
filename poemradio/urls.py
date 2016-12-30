"""poemradio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
import poem.views
import poemUser.views

urlpatterns = [
    url(r'^$', poem.views.mainView, name = "main"),
    # url(r'^signup/?$', poemUser.views.register, name='register'),
    # url(r'^login/?$', poemUser.views.user_login, name='login'),
    # url(r'^logout/?$', poemUser.views.user_logout, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('poemUser.urls', namespace = "user")),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('poem.urls', namespace="poem")),

]
