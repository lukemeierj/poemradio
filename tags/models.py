from __future__ import unicode_literals

from django.db import models

class Tag(models.Model):
	tagName = models.CharField(max_length=200, default = "")
	def __str__(self):
		return self.tagName
	