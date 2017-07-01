from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
# from .forms import UserForm, PoemUserForm, LogInForm
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import models
from django.urls import reverse
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe
from poem.models import Poem
from poemUser.models import PoemUser
import random
from time import time


@require_safe
def showUser(request, username):
    try:
        userObj = User.objects.get(username = username.lower())
    except User.DoesNotExist:
        return HttpResponse("User does not exist.")
    return render(request, 'poemUser/profile.html', {'poems': Poem.objects.filter(author = userObj.poemuser), 'thisUser': userObj})


#Style types: random, squenence, and curated
def getQueueJSON(request, username = "AnonymousUser", style= "dynamic", n =10):
    username = request.user.username or None
    if request.user.is_active:
        if style == "dynamic":
            style = "curated"
        poemSet = request.user.poemuser.getUnread()
    else:

        if style == "dynamic":
            style = "random"
        poemSet = Poem.objects.all()


    if style == "sequence":
        queue = PoemUser.getSequentialPoems(poemSet, n)
    elif style == "random":
        queue = PoemUser.getRandomPoems(poemSet, n)

    elif style == 'curated':
        queue = request.user.poemuser.suggestions(n)

    json = {'username': username, 'queue': queue}
    return json
def getQueue(request, username = "AnonymousUser", style= "dynamic", n =10):
    return JsonResponse(getQueueJSON(request, username, style, n))
