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






#Simply shows the first name of the user, or states that the user does not exist
@require_safe
def showUser(request, username):
    try:
        userObj = User.objects.get(username = username.lower())
    except User.DoesNotExist:
        return HttpResponse("User does not exist.")
    return HttpResponse("User: %s" % (userObj.first_name))

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

# def register(request):
#     # context = ReqestContext(request)

#     registered = False

#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         poemUser_form = PoemUserForm(data=request.POST)
#         if (user_form.is_valid() and poemUser_form.is_valid()):
#             if not User.objects.filter(username=user_form.cleaned_data['username'].lower()).exists():
#                 username = user_form.cleaned_data['username'].lower()
#                 password = user_form.cleaned_data['password']
#                 first_name = user_form.cleaned_data['first_name']
#                 last_name = user_form.cleaned_data['last_name']
#                 email     = user_form.cleaned_data['email']
#                 user          = User(username = username, last_name = last_name, first_name=first_name, email=email)
#                 user.set_password(password)
#                 user.save()
#                 # print(user.username)
#                 poemUser      = poemUser_form.save(commit=False)
#                 poemUser.user = user
#                 poemUser.save()
#                 registered    = True
#                 user = authenticate(username=username, password=password)
#                 if user:
#                     if user.is_active:
#                         login(request, user)
#                     else:
#                         # An inactive account was used - no logging in!
#                         return HttpResponse("Your account is disabled.")
#             else: 
#                 user_form.add_error('username', "User already exists.")
#         # else:
#             # print(poemUser_form.errors, user_form.errors)
        
#     else:
#         poemUser_form = PoemUserForm(request.POST or None)
#         user_form = UserForm(request.POST or None)


#     return render(request, 'poemUser/signup.html',
#             {'user_form': user_form, 'poemUser_form': poemUser_form, 'registered': registered})

# def user_login(request):
#     if request.GET.get('next'):
#             nextURL = request.GET.get('next')
#     else:
#         nextURL = '/'
#     if request.method == 'POST':
        
#         print(nextURL)
#         form = LogInForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data["username"].lower()
#             password = form.cleaned_data["password"]
#             user = authenticate(username=username, password=password)
#             if user:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponseRedirect(nextURL)
#                 else:
#                     # An inactive account was used - no logging in!
#                     return HttpResponse("Your account is disabled.")
#             else:
#                 # Bad login details were provided. So we can't log the user in.

#                	return render(request, './poemUser/login.html', {'form': form, 'invalid': True})
#     else:
#         form = LogInForm(None)
#         return render(request, './poemUser/login.html', {'form': form, 'invalid': False, 'next': nextURL})

# # @login_required(login_url = reverse_lazy('login'))
# def user_logout(request):
# 	logout(request)
# 	return HttpResponseRedirect(reverse('main'))

