from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils import timezone

class Poem(models.Model):
    author = models.ForeignKey('poemUser.PoemUser', on_delete=models.CASCADE, default = 1)
    title = models.CharField(max_length=200, default = "")
    text = models.TextField(default = "")
    upvotes = models.IntegerField(default = 0)
    novotes = models.IntegerField(default = 0)
    downvotes = models.IntegerField(default = 0)
    creation = models.DateTimeField('date published', default = timezone.now, blank = True)
    source = models.URLField(max_length=200, blank=True, null = True)
    tags = models.ManyToManyField('tags.Tag', default = None)
    comments = models.ManyToManyField('Comment', default = None, related_name = "comments")

    def getAvgVote(self):
        return (upvotes-downvotes)/float(sum((upvotes, downvotes, novotes)))
    def __str__(self):
    	return self.title


class Comment(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    text = models.TextField(default = "")
    ip = models.GenericIPAddressField()
    is_public = models.BooleanField(default = True)
    is_removed = models.BooleanField(default = False)
    submit_time = models.DateTimeField('date published', default = timezone.now, blank = True)
