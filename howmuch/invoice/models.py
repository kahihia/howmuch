from django.db import models
from django.contrib.auth.models import User

from howmuch.article.models import Assignment

class Charge(models.Model):
	owner = models.ForeignKey(User)
	period = models.CharField(max_length=8)
	assignment = models.OneToOneField(Assignment)
	date = models.DateField(auto_now_add=True)
	price =  models.IntegerField()
	commission = models.IntegerField(default=0)

	def __unicode__(self):
		return u'%s' % (self.assignment.article.title)

class Invoice(models.Model):
	owner = models.ForeignKey(User)
	period = models.CharField(max_length=8)
	reference = models.CharField(max_length=10, blank=True)
	charges = models.ManyToManyField(Charge)
	total = models.IntegerField(default=0)
	is_paid = models.BooleanField(default=False)

	def __unicode__(self):
		return u'%s' % (self.reference)


