from django.db import models
from django.contrib.auth.models import User

from howmuch.article.models import Assignment

class Invoice(models.Model):
	owner = models.ForeignKey(User)
	assignment = models.OneToOneField(Assignment)
	period = models.CharField(max_length=5)
	commission = models.IntegerField(default=0)
	is_paid = models.BooleanField(default=False)

	def __unicode__(self):
		return u'%s' % (self.assignment.title)