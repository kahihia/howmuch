from django.db import models
from django.contrib.auth.models import User

from howmuch.utils import get_timestamp

class Comment(models.Model):
	owner = models.ForeignKey(User, related_name="owner by comment")
	date = models.DateTimeField(auto_now_add=True)
	comment = models.CharField(max_length=255)

	def __unicode__(self):
		return u'%s' % (self.comment)

	def get_timestamp(self):
		return get_timestamp(self.date)