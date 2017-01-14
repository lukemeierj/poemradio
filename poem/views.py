from django.shortcuts import render, get_object_or_404
from poem.models import Poem
from poemUser.views import getQueueJSON
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from .forms import SubmitPoemForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe
from django.contrib.auth.models import User
from poemUser.models import PoemUser, Read
from allauth.account.models import EmailAddress
from django.utils import timezone



@require_safe
def showPoem(request, poemID):
    poemObj  = get_object_or_404(Poem, pk=poemID)
    try:
        vote = Read.objects.filter(poem_id=poemID).filter(owner=request.user.poemuser).get().vote;
    except (Read.DoesNotExist, AttributeError) as e:
        vote = 0;
    context  = {
        'poem': poemObj,
        'vote': vote,
    }

    return render(request, 'poem/poem.html', context)

@require_safe
def jsonPoem(request, poemID):

    json = {}

    if Poem.objects.filter(pk=poemID).exists():
        poemObj = Poem.objects.get(pk=poemID)
        json['error'] = False;
        iterable = vars(poemObj)
        for key in iterable:
            if (key != "_state"):
                json[key] = iterable[key]
        tempList = []
        # for tag in poemObj.tags.all():
        #     tempList.append(tag.id)
        # json["tags"] = tempList
    else: json["error"] = True
    response = JsonResponse(json)
    return response

@login_required(login_url = reverse_lazy('account_login'))
def submit(request):
    if request.method == "POST":
        form = SubmitPoemForm(request.POST)
        if form.is_valid():
            newPoem = form.save(commit = False)
            newPoem.author = request.user.poemuser
            newPoem.save()
            return HttpResponseRedirect(reverse_lazy('poem:showPoem', kwargs = {"poemID":newPoem.id}))

    else:
        form = SubmitPoemForm()
    verified = EmailAddress.objects.filter(user=request.user, verified=True).exists()
    if not verified:
        return HttpResponseRedirect("/accounts/email/?next=/submit") 
    return render(request, 'poem/submit.html', {'form': form, 'verified': verified })

    

@require_safe
def mainView(request):
    try:
        poemuser = request.user.poemuser
        print(poemuser.user.username)
    except (PoemUser.DoesNotExist, AttributeError):
        loggedin = False
        context = getQueueJSON(request)  
    else:
        loggedin = True
        context = getQueueJSON(request, username = poemuser.user.username)
    print(loggedin)
    print(context)
    return render(request, 'poem/index.html', context)

def markRead(request):
    if request.method == "GET":
        return HttpResponseRedirect("/")
    poemID = int(request.POST["poemID"])
    vote = int(request.POST['vote'])
    start = int(request.POST['start'])
    end = int(request.POST['end'])
    duration = (end-start)/1000
    print(request.POST['username'].lower())
    if request.POST['username'].lower() != "anonymoususer":
            try:
                poemuser = User.objects.get(username=request.POST['username'].lower()).poemuser
            except User.DoesNotExist:
                Http404("User does not exist")
            else:
                try: 
                    read = poemuser.reads.get(poem_id = poemID)
                except Read.DoesNotExist:
                    try:
                        poemObj = Poem.objects.get(pk = poemID)
                    except Poem.DoesNotExist:
                        raise Http404("Poem does not exist")
                    else:
                        read = Read(owner = poemuser, poem = poemObj, vote = vote, viewDuration = duration)
                        read.save()
                        read.addVote()
                        return HttpResponse("Success.")
                else:
                    print("Updating old")
                    read.updateReread(vote = vote, viewTime = timezone.now(), viewDuration = duration)
                    return HttpResponse("Success")
    else:
        return HttpResponse("Success.")
    raise Http404("Something is wrong")
                    


    
    

