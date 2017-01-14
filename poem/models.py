from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils import timezone
from poemradio import profanities
from tagging.registry import register
from tagging.fields import TagField


class Poem(models.Model):
    author = models.ForeignKey('poemUser.PoemUser', on_delete=models.CASCADE, default = 1)
    title = models.CharField(max_length=75, default = "")
    text = models.TextField(default = "")
    upvotes = models.IntegerField(default = 0)
    novotes = models.IntegerField(default = 0)
    downvotes = models.IntegerField(default = 0)
    creation = models.DateTimeField('date published', default = timezone.now, blank = True)
    source = models.URLField(max_length=200, blank=True, null = True)
    centered = models.BooleanField(default = False)
    comments = models.ManyToManyField('Comment', default = None, blank = True, related_name = "comments")
    flagged = models.BooleanField(default = False)
    profane = models.BooleanField(default = False)
    tags = TagField()


    def getAvgVote(self):
        return (upvotes-downvotes)/float(sum((upvotes, downvotes, novotes)))
    def getProfanity(self):
        splitWords = self.text.split() + self.title.split()
        if set(profanities.PROFANITIES).intersection(splitWords) or 'fuck' in splitWords:
            self.profane = True
        return self.profane
    def __str__(self):
    	return self.title

    def save(self, *args, **kwargs):
        self.profane = self.getProfanity()
        super(Poem, self).save(*args, **kwargs)



class Comment(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    text = models.TextField(default = "")
    ip = models.GenericIPAddressField()
    is_public = models.BooleanField(default = True)
    is_removed = models.BooleanField(default = False)
    submit_time = models.DateTimeField('date published', default = timezone.now, blank = True)
