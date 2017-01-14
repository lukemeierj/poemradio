from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from poem.models import Poem
from django.utils import timezone
import random
import math
import operator
from tagging.fields import TagField


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
    preferences = TagField()
    similar = models.ManyToManyField('self', default = [])
    agreed_tos = models.BooleanField(default = False)
    promo_email = models.BooleanField(default = False)

    
    #Returns lists in tuple, (selfVotes, foreignVotes)
    def getSharedReads(self, foreignPoemUserObj):
        commonPoems = Poem.objects.filter(reads__owner = self).filter(reads__owner = foreignPoemUserObj).filter(flagged = False)
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
        else: 
            return 0

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
        unread = Poem.objects.exclude(reads__owner = self).filter(flagged=False)
        if(self.safeMode):
            unread = unread.filter(profane = False)
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
        
        neighborlyPoems = Poem.objects.filter(
            reads__owner__in = self.similar.all()).exclude(reads__vote=-1).exclude(reads__owner = self).exclude(flagged = True)
        if(self.safeMode):
            neighborlyPoems = neighborlyPoems.filter(profane=False)

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
