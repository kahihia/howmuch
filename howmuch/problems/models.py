from django.db import models
from django.contrib.auth.models import User

from howmuch.article.models import Assignment

class Problem(models.Model):
	owner = models.ForeignKey(User)
	assignment = models.ForeignKey(Assignment)
	date = models.DateTimeField(auto_now_add=True)
	description = models.CharField(max_length=1024)
	is_solved = models.BooleanField(default=False)
	status = models.CharField(max_length=24, default='In Process')

	def __unicode__(self):
		return '%s' % (self.description)


class Reply(models.Model):
	admin = models.ForeignKey(User)
	problem = models.ForeignKey(Problem)
	date = models.DateTimeField(auto_now_add=True)
	response = models.CharField(max_length=1024)

	def __unicode__(self):
		return '%s' % (self.response)


class Action(models.Model):
	problem = models.ForeignKey(Problem)
	date = models.DateTimeField(auto_now_add=True)
	action = models.CharField(max_length=1024)

	def __unicode__(self):
		return '%s' % (self.action)





