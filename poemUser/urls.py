from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^(?P<username>[a-zA-Z0-9_#+-.]*)/?$', views.showUser, name='showUser'),
    url(r'^(?P<username>[a-zA-Z0-9_#+-.]*)/getQueue/?$', views.getQueue, name='getQueue'),
]