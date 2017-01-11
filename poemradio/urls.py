from django.conf.urls import include, url
from django.contrib import admin
import poem.views
import poemUser.views
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', poem.views.mainView, name = "main"),
    #old signup protocol
    # url(r'^signup/?$', poemUser.views.register, name='register'),
    # url(r'^login/?$', poemUser.views.user_login, name='login'),
    # url(r'^logout/?$', poemUser.views.user_logout, name='logout'),
    url(r'^termsandprivacy', TemplateView.as_view(template_name='poem/termsandprivacy.html')),
    url(r'^about', TemplateView.as_view(template_name='poem/about.html')),
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('poemUser.urls', namespace = "user")),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('poem.urls', namespace="poem")),

]
