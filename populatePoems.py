import sys, os
sys.path.append('/Users/LittleMac/Code/poemradio-django/poemradio')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings
import django
django.setup()
from django.contrib.auth.models import User
from poemUser import models
import poem.models

def getPoems(filename):
    with open(filename, 'rb') as f:
        text = b''
        for line in f:
            if b':,:' in line:
                author = line.split(b':,:')[0]
            elif b':n:' in line:
                tempText = text
                text = b''
                yield(author, tempText)
            else:
                text += line


def createUser(username, password, first, last, email):
    # user = User.objects.create_user(username, email, password)
    if not User.objects.filter(username = username):
        user = User()
        user.username = username.lower()
        user.email = email
        user.password = password
        user.last_name = last
        user.first_name = first
        user.save()
        poemuser = models.PoemUser()
        poemuser.user = user
        poemuser.save()
        user.save()
        return None
def createPoem(text, nameOfUser, source = 'http://www.poemhunter.com'):
    newPoem = poem.models.Poem()
    newPoem.text = text
    user = User.objects.get(username=nameOfUser)
    newPoem.author = user.poemuser
    newPoem.source = source
    newPoem.title = nameOfUser
    newPoem.save()
    return None
def addPoems():
    for author, text in getPoems('classicPoem.csv'):
        author = author.decode('utf-8')
        last = author.split()[-1]
        first = author.split()[0]
        username = last
        password = "Cl@ss*cB@yes"
        email = "test@test.com"
        text = text.decode('utf-8')
        createUser(username, password, first, last, email)
        createPoem(text, last)

        print(author.encode('utf-8'))


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
addPoems()



