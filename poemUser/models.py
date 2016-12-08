from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from poem.models import Poem
from django.utils import timezone
import random
import json
#import time
#from sklearn import (preprocessing, metrics)
import math
import operator
#import numpy as np



"""
def popCoefficient(x, k=.5):
    return (2/np.pi)*np.arctan((np.pi/2)*k*x)

def calcSimilarity(array1, array2, array1TotalInt = None, array2TotalInt = None, k1 = .5):
    array1 = preprocessing.scale(array1)
    array2 = preprocessing.scale(array2)
    similarity_raw = 1/(1+metrics.mean_squared_error(array1, array2))
    if array1TotalInt and array2TotalInt:
        similarity = similarity_raw*popCoefficient(5*(len(array1)/array1TotalInt)*(len(array2)/array2TotalInt), k1)
        return similarity
    return similarity_raw
"""
def dot_product(v1, v2):
    return sum(map(operator.mul, v1, v2))
def cosSimilarity(v1, v2, standardize = False):
    if(standardize):
        v1 = preprocessing.scale(v1)
        v2 = preprocessing.scale(v2)
    prod = dot_product(v1, v2)
    len1 = math.sqrt(dot_product(v1, v1))
    len2 = math.sqrt(dot_product(v2, v2))
    if(len1!=0 and len2!=0):
        return prod / (len1 * len2)
    else: return 0

    
class PoemUser(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    safeMode = models.BooleanField(default = False)
    preferences = models.ManyToManyField('tags.Tag', blank=True)
    similar = models.ManyToManyField('self', default = [])
    
    #Returns lists in tuple, (selfVotes, foreignVotes)

    def getSharedReads(self, foreignPoemUserObj):
        commonPoems = Poem.objects.filter(reads__owner = self).filter(reads__owner = foreignPoemUserObj)
        selfReads = Read.objects.filter(poem__in=commonPoems).filter(owner = self)
        foreignReads = Read.objects.filter(poem__in=commonPoems).filter(owner = foreignPoemUserObj)
        return (selfReads, foreignReads)

    def getSimilarity(self, foreignPoemUserObj):
        selfPoems, foreignPoems = self.getSharedReads(foreignPoemUserObj)
        if selfPoems and foreignPoems:
            selfVotes = [poem.vote for poem in selfPoems]
            foreignVotes = [poem.vote for poem in foreignPoems]
            similarity = cosSimilarity(selfVotes, foreignVotes)
            return similarity
        else: return 0
    def nearestNeighbors(self, k = 5):
        neighbors = []
        for poemuser in PoemUser.objects.all():
            if poemuser != self:

                neighbors.append((poemuser, self.getSimilarity(poemuser)))

        neighbors.sort(key = lambda tuple: tuple[1], reverse = True)

        nearest = neighbors[0:min(k, len(neighbors))]
        print(nearest)
        return nearest
    def updateSimilars(self, near = None):
        if(near==None):
            near = self.nearestNeighbors()
        self.similar.add(*[pair[0] for pair in near])
        self.save()



    def getUnread(self):
        unread = Poem.objects.exclude(reads__owner = self)
        return unread
    @classmethod
    #TODO:  OPTIMIZE RANDOM FOR ALL()
    def getRandomPoems(cls, poemSet, n = 10):
        indicies = []
        queue = []
        randomIndices = random.sample(range(0, len(poemSet)), n)
        return [poemSet[i].id for i in randomIndices]
    @classmethod
    def getSequentialPoems(cls, poemSet, n = 10):
        queue = poemSet[:n]
        queue = [poem.pk for poem in queue]
        return queue
    def suggestions(self, n = 10, *args, **kwargs):
        if (self.similar.exists()):
            neighbors = self.nearestNeighbors()
            self.updateSimilars(neighbors)
        neighborlyPoems = Poem.objects.filter(reads__owner__in = self.similar.all()).exclude(reads__owner = self)
        if(n<=neighborlyPoems.count()):
            randomIndices = random.sample(range(0, neighborlyPoems.count()), n)
            return [neighborlyPoems[i].id for i in randomIndices]
        else:
            semiNeighborlyPoems = [poem.id for poem in neighborlyPoems]+list(self.getRandomPoems(Poem.objects.all(), n-neighborlyPoems.count()))
            return [poem for poem in semiNeighborlyPoems]
        
        


    def __str__(self):
        try:
            return self.user.username
        except User.DoesNotExist: return "Undefined"
    
class Read(models.Model):
    owner = models.ForeignKey(PoemUser, on_delete=models.CASCADE, related_name = 'reads', blank=True, null=True)
    viewTime = models.DateTimeField('date viewed', default =  timezone.now)
    poem = models.ForeignKey('poem.Poem', on_delete=models.CASCADE, related_name = 'reads')
    viewDuration = models.FloatField(default = 0)
    vote = models.IntegerField(default = 0)
    def addVote(self, vote = None, commit = True):
        if vote is None:
            # print("Vote is None")
            vote = self.vote
        # print(vote)
        if vote == 0:
            # print("One more novote")
            self.poem.novotes += 1
        elif vote == 1:
            # print("One more upvote")

            self.poem.upvotes += 1
        elif vote == -1:
            # print("One more downvote")

            self.poem.downvotes += 1
        if commit: 
            self.poem.save()
        return None
    def removeOldVote(self, commit = True):
        if self.vote == 0:
            # print("One fewer novote")
            self.poem.novotes -= 1
        elif self.vote == 1:
            # print("One fewer upvote")

            self.poem.upvotes -= 1
        elif self.vote == -1:
            # print("One fewer downvote")

            self.poem.downvotes -= 1
        if commit:
            self.poem.save()
        return None
    def updateReread(self, vote, viewTime, viewDuration):
        self.viewTime = viewTime
        self.viewDuration = viewDuration
        if vote != self.vote:
            self.removeOldVote(commit = False)
            self.addVote(vote)
            self.vote = vote
            self.save()

    def delete(self, *args, **kwargs):
        self.removeOldVote()
        super(Read, self).delete(*args, **kwargs)

    def __str__(self):
        return ("%s: %s" % (self.owner.user.username, self.poem))
