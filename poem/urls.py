from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^markRead/?$', views.markRead, name='markRead'),
    url(r'^(?P<poemID>[0-9]*)/?$', views.showPoem, name='showPoem'),
    url(r'^json/(?P<poemID>[0-9]*)/?$', views.jsonPoem, name='jsonPoem'),
   	url(r'^submit/?$', views.submit, name='submit'),

]
