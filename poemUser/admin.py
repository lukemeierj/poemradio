from django.contrib import admin

from .models import PoemUser, Read

admin.site.register(PoemUser)
admin.site.register(Read)